from  kolibri_report.report import Report
from kolibri.model_trainer import ModelTrainer,ModelConfig
from kolibri.model_loader import ModelLoader
import os
import pandas as pd

data = pd.read_csv('/Users/aneruthmohanasundaram/Documents/Office/kolibri_doc/wine.csv')

confg = {}
confg['do-lower-case'] = True
confg['language'] = 'en'
confg['filter-stopwords'] = True
confg["model"] = 'RandomForestClassifier'
confg["n_estimators"] = 100
confg['output-folder'] = '/Users/aneruthmohanasundaram/Documents/Office/kolibri_doc/demos'
confg['pipeline']= ['SklearnEstimator']
confg['target']= 'type'

X = data.drop('type',axis=1)
y = data.type

trainer=ModelTrainer(ModelConfig(confg))

trainer.fit(X, y)

model_directory = trainer.persist(confg['output-folder'], fixed_model_name="current")
model_interpreter = ModelLoader.load(os.path.join(confg['output-folder'], 'current'))

app_report = Report(data)
app_report.run()
os.system(f"streamlit run {__file__}")