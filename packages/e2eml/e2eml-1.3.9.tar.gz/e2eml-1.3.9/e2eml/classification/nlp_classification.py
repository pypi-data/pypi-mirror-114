import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler, Dataset
import transformers
from transformers import AutoModel, BertTokenizerFast, AdamW, BertModel
from transformers import get_linear_schedule_with_warmup
from sklearn.metrics import matthews_corrcoef, mean_squared_error
from tqdm import tqdm
import os
import gc
from sklearn.utils.class_weight import compute_class_weight
from e2eml.full_processing import postprocessing
import random

# specify GPU
scaler = torch.cuda.amp.GradScaler()  # GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class ClassificationModels(postprocessing.FullPipeline):
    """
    This class stores all model training and prediction methods for classification tasks.
    This class stores all pipeline relevant information (inherited from cpu preprocessing).
    The attribute "df_dict" always holds train and test as well as
    to predict data. The attribute "preprocess_decisions" stores encoders and other information generated during the
    model training. The attributes "predicted_classes" and "predicted_probs" store dictionaries (model names are dictionary keys)
    with predicted classes and probabilities (classification tasks) while "predicted_values" stores regression based
    predictions. The attribute "evaluation_scores" keeps track of model evaluation metrics (in dictionary format).
    :param datasource: Expects a Pandas dataframe (containing the target feature as a column)
    :param target_variable: Name of the target feature's column within the datasource dataframe.
    :param date_columns: Date columns can be passed as lists additionally for respective preprocessing. If not provided
    e2eml will try to detect datetime columns automatically. Date format is expected as YYYY-MM-DD anyway.
    :param categorical_columns: Categorical columns can be passed as lists additionally for respective preprocessing.
    If not provided e2eml will try to detect categorical columns automatically.
    :param nlp_columns: NLP columns can be passed specifically. This only makes sense, if the chosen blueprint runs under 'nlp' processing.
    If NLP columns are not declared, categorical columns will be interpreted as such.
    :param unique_identifier: A unique identifier (i.e. an ID column) can be passed as well to preserve this information
     for later processing.
    :param ml_task: Can be 'binary', 'multiclass' or 'regression'. On default will be determined automatically.
    :param preferred_training_mode: Must be 'cpu', if e2eml has been installed into an environment without LGBM and Xgboost on GPU.
    Can be set to 'gpu', if LGBM and Xgboost have been installed with GPU support. The default 'auto' will detect GPU support
    and optimize accordingly. (Default: 'auto')
    :param logging_file_path: Preferred location to save the log file. Will otherwise stored in the current folder.
    :param low_memory_mode: Adds a preprocessing feature to reduce dataframe memory footprint. Will lead to a loss in
    model performance. Will be extended by further memory savings features in future releases.
    However we highly recommend GPU usage to heavily decrease model training times.
    """

    def import_transformer_model_tokenizer(self, transformer_chosen=None):
        if not transformer_chosen:
            transformer_chosen = 'bert-base-uncased'
        else:
            transformer_chosen = self.transformer_chosen

        if self.transformer_model_load_from_path:
            bert = AutoModel.from_pretrained(f"{self.transformer_model_load_from_path}",
                                             output_attentions=False,  # Whether the model returns attentions weights.
                                             output_hidden_states=False)
            tokenizer = transformers.BertTokenizer.from_pretrained(f"{self.transformer_model_load_from_path}")
        else:
            # import BERT-base pretrained model
            bert = AutoModel.from_pretrained(transformer_chosen)
            # Load the BERT tokenizer
            tokenizer = BertTokenizerFast.from_pretrained(transformer_chosen)
        if "nlp_transformers" in self.preprocess_decisions:
            pass
        else:
            self.preprocess_decisions[f"nlp_transformers"] = {}

        self.preprocess_decisions[f"nlp_transformers"][f"transformer_model_{transformer_chosen}"] = bert
        self.preprocess_decisions[f"nlp_transformers"][f"transformer_tokenizer_{transformer_chosen}"] = tokenizer

    def check_max_sentence_length(self, text_columns=None):
        if self.prediction_mode:
            pass
        else:
            X_train, X_test, Y_train, Y_test = self.unpack_test_train_dict()
            text_columns = self.check_for_nlp_transformer_columns(text_columns=text_columns, return_list=True)
            seq_len = [len(i.split()) for i in X_train[text_columns]]
            pd.Series(seq_len).hist(bins=30)
            self.preprocess_decisions[f"nlp_transformers"][f"max_sentence_len"] = max(seq_len)

    def reset_indices(self, mode='fit'):
        if mode == 'transform':
            self.dataframe = self.dataframe.reset_index(drop=True)
            return self.dataframe
        elif mode == 'fit':
            X_train, X_test, Y_train, Y_test = self.unpack_test_train_dict()
            X_train[self.target_variable] = Y_train
            X_test[self.target_variable] = Y_test
            X_train = X_train.reset_index(drop=True)
            X_test = X_test.reset_index(drop=True)
            Y_train = X_train[self.target_variable]
            Y_test = X_test[self.target_variable]
            X_train.drop(self.target_variable, axis=1)
            X_test.drop(self.target_variable, axis=1)
            return self.wrap_test_train_to_dict(X_train, X_test, Y_train, Y_test)
        else:
            print("Please chose either 'fit' or 'transform'.")


class BERTDataSet(Dataset):
    def __init__(self, sentences, targets, tokenizer):
        self.sentences = sentences
        self.targets = targets
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, idx):
        sentence = str(self.sentences[idx])
        target = self.targets[idx]
        inputs = self.tokenizer.encode_plus(
            sentence,
            None,
            add_special_tokens=True,
            padding='max_length',
            # return_token_type_ids=True,
            truncation=True
        )
        ids = inputs['input_ids']
        mask = inputs['attention_mask']
        token_type_ids = inputs["token_type_ids"]

        return {
            'ids': torch.tensor(ids, dtype=torch.long),
            'mask': torch.tensor(mask, dtype=torch.long),
            'token_type_ids': torch.tensor(token_type_ids, dtype=torch.long),
            'target': torch.tensor(target, dtype=torch.long)
        }


class BERTClass(torch.nn.Module):
    def __init__(self, transformer, num_classes):
        super(BERTClass, self).__init__()
        self.bert = BertModel.from_pretrained("bert-base-uncased", return_dict=False)
        self.dropout = nn.Dropout(0.3)
        self.classifier = torch.nn.Linear(768, num_classes)

    def forward(self, input_ids, token_type_ids, attention_mask):
        _, pooled_output = self.bert(input_ids, token_type_ids, attention_mask)
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        return logits


class NlpModel(ClassificationModels, BERTDataSet, BERTClass):
    def create_train_dataset(self):
        X_train, X_test, Y_train, Y_test = self.unpack_test_train_dict()
        tokenizer = self.preprocess_decisions[f"nlp_transformers"][f"transformer_tokenizer_{self.transformer_chosen}"]
        train_dataset = BERTDataSet(X_train[self.nlp_transformer_columns], Y_train, tokenizer)
        return train_dataset

    def create_test_dataset(self):
        X_train, X_test, Y_train, Y_test = self.unpack_test_train_dict()
        tokenizer = self.preprocess_decisions[f"nlp_transformers"][f"transformer_tokenizer_{self.transformer_chosen}"]
        test_dataset = BERTDataSet(X_test[self.nlp_transformer_columns], Y_test, tokenizer)
        return test_dataset

    def create_pred_dataset(self):
        self.dataframe[self.target_variable] = 999  # creating dummy column
        self.reset_indices(mode='transform')
        dummy_target = self.dataframe[self.target_variable]
        self.dataframe.drop(self.target_variable, axis=1)
        tokenizer = self.preprocess_decisions[f"nlp_transformers"][f"transformer_tokenizer_{self.transformer_chosen}"]
        pred_dataset = BERTDataSet(self.dataframe[self.nlp_transformer_columns], dummy_target, tokenizer)
        return pred_dataset

    def create_train_dataloader(self, train_batch_size=None, workers=None):
        if train_batch_size:
            pass
        else:
            train_batch_size = self.transformer_settings["train_batch_size"]

        if workers:
            pass
        else:
            workers = self.transformer_settings["num_workers"]
        train_dataset = self.create_train_dataset()
        train_dataloader = DataLoader(train_dataset, batch_size=train_batch_size, shuffle=True, num_workers=workers,
                                      pin_memory=True)
        return train_dataloader

    def create_test_dataloader(self, test_batch_size=None, workers=None):
        if test_batch_size:
            pass
        else:
            test_batch_size = self.transformer_settings["test_batch_size"]

        if workers:
            pass
        else:
            workers = self.transformer_settings["num_workers"]
        test_dataset = self.create_test_dataset()
        test_dataloader = DataLoader(test_dataset, batch_size=test_batch_size, shuffle=True, num_workers=workers,
                                     pin_memory=True)
        return test_dataloader

    def pred_dataloader(self, pred_batch_size=None, workers=None):
        if pred_batch_size:
            pass
        else:
            pred_batch_size = self.transformer_settings["pred_batch_size"]

        if workers:
            pass
        else:
            workers = self.transformer_settings["num_workers"]
        pred_dataset = self.create_pred_dataset()
        pred_dataloader = DataLoader(pred_dataset, batch_size=pred_batch_size, shuffle=False, num_workers=workers,
                                     pin_memory=True)
        return pred_dataloader

    def loss_fn(self, output, target):
        return torch.nn.CrossEntropyLoss()(output, target)

    # nn.MultiMarginLoss, #CrossEntropyLoss, #MSELoss

    def model_setup(self, epochs=None):
        if self.prediction_mode:
            pass
        else:
            X_train, X_test, Y_train, Y_test = self.unpack_test_train_dict()
            model = BERTClass(
                self.preprocess_decisions[f"nlp_transformers"][f"transformer_model_{self.transformer_chosen}"],
                self.num_classes)
            model.to(device)
            model.train()
            LR = 2e-5
            optimizer = AdamW(model.parameters(), LR, betas=(0.9, 0.999), weight_decay=1e-2)
            if epochs:
                pass
            else:
                epochs = self.transformer_settings["epochs"]
            epochs = epochs
            train_steps = int(len(X_train) / self.transformer_settings["train_batch_size"] * epochs)
            num_steps = int(train_steps * 0.1)
            scheduler = get_linear_schedule_with_warmup(optimizer, num_steps, train_steps)
            self.preprocess_decisions[f"nlp_transformers"][f"sheduler_{self.transformer_chosen}"] = scheduler
            return model, optimizer, train_steps, num_steps, scheduler

    def training(self, train_dataloader, model, optimizer, scheduler):
        model.train()
        allpreds = []
        alltargets = []

        for a in train_dataloader:
            losses = []
            optimizer.zero_grad()

            with torch.cuda.amp.autocast():
                ids = a["ids"].to(device)
                mask = a["mask"].to(device)
                target = a["target"].to(device)
                token_type_ids = a["token_type_ids"].to(device)

                output = model(ids, mask, token_type_ids)
                loss = self.loss_fn(output, target)

                # For scoring
                losses.append(loss.item() / len(output))
                allpreds.append(output.detach().cpu().numpy())
                alltargets.append(target.detach().cpu().numpy())

            scaler.scale(loss).backward()  # backwards of loss
            scaler.step(optimizer)  # Update optimizer
            scaler.update()  # scaler update
            scheduler.step()  # Update learning rate schedule

            # Combine dataloader minutes

        allpreds = np.concatenate(allpreds)
        allpreds = np.asarray([np.argmax(line) for line in allpreds])
        alltargets = np.concatenate(alltargets)

        # I don't use loss, but I collect it
        losses = np.mean(losses)
        # Score with rmse
        print(alltargets.shape)
        print("-------------------------")
        print(allpreds.shape)
        train_rme_loss = matthews_corrcoef(alltargets, allpreds)

        return losses, train_rme_loss

    def validating(self, valid_dataloader, model):

        model.eval()
        allpreds = []
        alltargets = []

        for a in valid_dataloader:
            losses = []

            with torch.no_grad():
                ids = a["ids"].to(device)
                mask = a["mask"].to(device)
                target = a["target"].to(device)
                token_type_ids = a["token_type_ids"].to(device)

                output = model(ids, mask, token_type_ids)
                loss = self.loss_fn(output, target)
                # For scoring
                losses.append(loss.item() / len(output))
                allpreds.append(output.detach().cpu().numpy())
                alltargets.append(target.detach().squeeze(-1).cpu().numpy())
                # Combine dataloader minutes

        allpreds = np.concatenate(allpreds)
        allpreds = np.asarray([np.argmax(line) for line in allpreds])
        alltargets = np.concatenate(alltargets)

        # I don't use loss, but I collect it
        losses = np.mean(losses)
        # Score with rmse
        valid_rme_loss = matthews_corrcoef(alltargets, allpreds)

        return allpreds, losses, valid_rme_loss

    def predicting(self, pred_dataloader, model, pathes):
        allpreds = []
        model_no = 0
        mode_cols = []
        for m_path in pathes:
            state = torch.load(m_path)
            model.load_state_dict(state["state_dict"])
            model.to(device)
            model.eval()
            preds = []
            allvalloss = 0
            with torch.no_grad():
                for a in pred_dataloader:
                    ids = a["ids"].to(device)
                    mask = a["mask"].to(device)
                    token_type_ids = a["token_type_ids"].to(device)
                    output = model(ids, mask, token_type_ids)

                    preds.append(output.detach().cpu().numpy())

                preds = np.concatenate(preds)
                print("-----preds shape-------")
                print(preds.shape)
                pred_classes = np.argmax(preds, axis=1).flatten()
                self.dataframe[f"preds_model{model_no}"] = pred_classes
                mode_cols.append(f"preds_model{model_no}")
                print("-----pred classes shape-------")
                print(pred_classes.shape)
                print(pred_classes)
                print("------------")
                allpreds.append(preds)
                print(allpreds)
                model_no += 1
            del state
            torch.cuda.empty_cache()
            _ = gc.collect()
            print(allpreds)
            allpreds = np.argmax(preds, axis=1).flatten()
            print("XXXXXXXXXX")
            print(allpreds)
            allpreds = allpreds.tolist()
        return allpreds, mode_cols

    def load_model_states(self, path=None):
        if path:
            pass
        else:
            path = os.getcwd()
        if self.prediction_mode:
            pthes = [os.path.join(f"{path}/", s) for s in os.listdir(f"{path}/") if ".pth" in s]
            return pthes
        else:
            pthes = [os.path.join(f"{path}/", s) for s in os.listdir(f"{path}/") if ".pth" in s]
            return pthes

    def transformer_train(self):
        if self.prediction_mode:
            pass
        else:
            X_train, X_test, Y_train, Y_test = self.unpack_test_train_dict()
            train_dataloader = self.create_train_dataloader()
            test_dataloader = self.create_test_dataloader()
            model, optimizer, train_steps, num_steps, scheduler = self.model_setup()
            scheduler = get_linear_schedule_with_warmup(optimizer, num_steps, train_steps)

            trainlosses = []
            vallosses = []
            bestscore = None
            trainscores = []
            validscores = []

            for epoch in tqdm(range(self.transformer_settings["epochs"])):
                print("---------------" + str(epoch) + "start-------------")
                trainloss, trainscore = self.training(train_dataloader, model, optimizer, scheduler)
                trainlosses.append(trainloss)
                trainscores.append(trainscore)
                print("trainscore is " + str(trainscore))
                preds, validloss, valscore = self.validating(test_dataloader, model)
                vallosses.append(validloss)
                validscores.append(valscore)

                print("valscore is " + str(valscore))
                if bestscore is None:
                    bestscore = valscore
                    print("Save first model")
                    state = {
                        'state_dict': model.state_dict(),
                        'optimizer_dict': optimizer.state_dict(),
                        "bestscore": bestscore
                    }
                    torch.save(state, "model0.pth")

                elif bestscore > valscore:
                    bestscore = valscore
                    print("found better point")
                    state = {
                        'state_dict': model.state_dict(),
                        'optimizer_dict': optimizer.state_dict(),
                        "bestscore": bestscore
                    }
                    torch.save(state, "model0.pth")
                else:
                    pass

            bestscores = []
            bestscores.append(bestscore)

            for fold in range(1, 5):

                # initializing the data
                train_dataloader = self.create_train_dataloader()
                test_dataloader = self.create_test_dataloader()

                model = BERTClass(
                    self.preprocess_decisions[f"nlp_transformers"][f"transformer_model_{self.transformer_chosen}"],
                    self.num_classes)
                model.to(device)
                LR = 2e-5
                optimizer = AdamW(model.parameters(), LR, betas=(0.9, 0.999), weight_decay=1e-2)  # AdamW optimizer
                train_steps = int(
                    len(X_train) / self.transformer_settings["train_batch_size"] * self.transformer_settings["epochs"])
                num_steps = int(train_steps * 0.1)
                scheduler = get_linear_schedule_with_warmup(optimizer, num_steps, train_steps)

                trainlosses = []
                vallosses = []
                bestscore = None
                trainscores = []
                validscores = []

                for epoch in tqdm(range(self.transformer_settings["epochs"])):
                    print("---------------" + str(epoch) + "start-------------")
                    trainloss, trainscore = self.training(train_dataloader, model, optimizer, scheduler)
                    trainlosses.append(trainloss)
                    trainscores.append(trainscore)

                    print("trainscore is " + str(trainscore))
                    preds, validloss, valscore = self.validating(test_dataloader, model)

                    vallosses.append(validloss)
                    validscores.append(valscore)
                    print("valscore is " + str(valscore))

                    if bestscore is None:
                        bestscore = valscore
                        print("Save first model")
                        state = {
                            'state_dict': model.state_dict(),
                            'optimizer_dict': optimizer.state_dict(),
                            "bestscore": bestscore
                        }
                        torch.save(state, "model" + str(fold) + ".pth")
                    elif bestscore > valscore:
                        bestscore = valscore
                        print("found better point")
                        state = {
                            'state_dict': model.state_dict(),
                            'optimizer_dict': optimizer.state_dict(),
                            "bestscore": bestscore
                        }
                        torch.save(state, "model" + str(fold) + ".pth")
                    else:
                        pass
                bestscores.append(bestscore)

            del model, optimizer, scheduler
            _ = gc.collect()

    def transformer_predict(self):
        model = BERTClass(
            self.preprocess_decisions[f"nlp_transformers"][f"transformer_model_{self.transformer_chosen}"],
            self.num_classes)
        pthes = self.load_model_states()
        print(pthes)
        pred_dataloader = self.pred_dataloader()
        allpreds, mode_cols = self.predicting(pred_dataloader, model, pthes)
        #print(allpreds)
        #findf = pd.DataFrame(allpreds)
        #findf = findf.T
        self.dataframe["majority_class"] = self.dataframe[mode_cols].mode(axis=1)[0]
        print(self.dataframe["majority_class"])
        print("---------------")
        print(self.dataframe)
        self.predicted_classes['nlp_transformer'] = self.dataframe["majority_class"]
