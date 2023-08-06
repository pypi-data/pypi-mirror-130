from abc import ABC,abstractclassmethod
import streamlit as st
import matplotlib.pyplot as plt
from kolibri.model_trainer import ModelTrainer,ModelConfig
import seaborn as sns,os
class KolibriImplements(ABC):
    """
    This is a abstract method for report implementation.
    """
    @abstractclassmethod
    def Data(self):
        pass

    @abstractclassmethod
    def Visualise(self):
        pass

    @abstractclassmethod
    def kolibriInteg(self):
        pass
    
    @abstractclassmethod
    def featureInteraction(self):
        pass

    @abstractclassmethod
    def run(self):
        pass

class Report(KolibriImplements):
    """
    A class which creates us the dashboard for our model and plots all the score and graph. This requires
    dataset as important parameter.
    """
    def __init__(self,data=None) -> None:
        self.dataset = data
        # self.target = target
        pass
    
    def Data(self):
        '''
        This method displays description of the model, Model Version​,Kolibri Version​,Owner​ and Trained at​.
        '''
        # st.dataframe(self.dataset,width=1000)
        st.table(self.dataset[:21])
    
    def Visualise(self):
        st.title('Visualising our dataset!!')
        # if we choose the options we get our output result as list
        col1,col2 = st.columns([2,2])
        with col1:
            st.write(''' #### Class comparison for our dataset''')
            sns.countplot(x='type',data=self.dataset)
            st.pyplot()
            with st.expander("See explanation"):
                st.write("""The chart above shows some numbers class present in our dataset.""")
        with col2:
            st.write(''' #### Heatmap for our dataset''')
            sns.heatmap(self.dataset.corr(),cmap='Greens')
            st.pyplot()
            with st.expander("See explanation"):
                st.write("""The chart above shows some numbers class present in our dataset.""")
    
    def kolibriInteg(self):
        pass
    
    def featureInteraction(self):
        """Checking our feature how it interacts with other feature. We provde you a dropbox 
        functionality and then you can analyse the interactn fo the features.
        """
        st.title('Feature Interactions for our datset!!')
        cols = self.dataset.columns.unique().tolist()[:12]

        
    
    def run(self):
        st.set_page_config(layout='wide')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        col1,col2,col3,col4,col5 = st.columns([3,3,3,3,3])
        overview = col1.button('Overview')
        data_visualise = col2.button('Visualise your data')
        model_analyse = col3.button('Model Analysis')
        roc = col4.button('ROC Curves')
        feature_interaction = col5.button("Feature Interaction")
    
        # If we click the button name then the respective mapped function will display
        if overview:
            st.title("View Data")
            st.header("This is a sample view method which will be changed in future")
            self.Data()
        
        elif data_visualise:
            self.Visualise()
        
        elif model_analyse:
            st.title("yet to implement")
        
        elif roc:
            st.title("yet to implement")
        
        elif feature_interaction:
            self.featureInteraction()

        os.system(f"streamlit run {__file__}")

# if __name__ == '__main__':
#     import pandas as pd
#     data = pd.read_csv('/Users/aneruthmohanasundaram/Documents/Office/kolibri_doc/wine.csv')
#     app = Report(data)
#     app.run()