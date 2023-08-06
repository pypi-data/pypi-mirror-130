from abc import ABC,abstractclassmethod
import streamlit as st
import matplotlib.pyplot as plt
from kolibri.model_trainer import ModelTrainer,ModelConfig

class Report(ABC):
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
        import seaborn as sns
        st.title('Visualising our dataset!!')
        # if we choose the options we get our output result as list
        with st.container():
            st.write(''' #### Class comparison for our dataset''')
            class_count =self.dataset.type.value_counts()
            st.bar_chart(class_count)
            with st.expander("See explanation"):
                st.write("""The chart above shows some numbers class present in our dataset.""")
        with st.container():
            st.write(''' #### Heatmap for our dataset''')
            plt.figure(figsize=(6,7))
            sns.heatmap(self.dataset.corr(),cmap='Greens')
            st.pyplot()
            with st.expander("See explanation"):
                st.write("""The chart above shows some numbers class present in our dataset.""")
    
    
    def kolibriInteg(self):
        pass
    
    
    
    def run(self):
        st.set_page_config(layout='wide')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        col1,col2,col3,col4,col5 = st.columns([1,1,1,1,1])
        overview = col1.button('Overview')
        data_visualise = col2.button('Visualise your data')
        model_analyse = col3.button('Model Analysis')
        roc = col4.button('ROC Curves')
        feature_interaction = col5.button("Feature Interaction")
    
        # Drodown to select the page to run  
        if overview:
            st.title("View Data")
            self.Data()
        
        elif data_visualise:
            self.Visualise()
        
        elif model_analyse:
            st.title("yet to implement")
        
        elif roc:
            st.title("yet to implement")
        
        elif feature_interaction:
            st.title("yet to implement")