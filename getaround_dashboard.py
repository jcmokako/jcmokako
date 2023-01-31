
import streamlit as st  # 🎈 data web app development
import time  # to simulate a real time data, time loop
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
#import plotly.express as px  # interactive charts

st.set_page_config(
    page_title="Getaround delay analysis",
    page_icon="✅",
    layout="wide",
)

## décommentez la 2ème ligne si vous n'êtes pas sur colab ou commentez la si vous êtes sur collab
colab = True
colab = False

## détermination du path
mypath = ''
if colab:
    from sys import path
    from google.colab import drive
    drive.mount('/content/drive')
    path.insert(0,'/content/drive/MyDrive/Getaround/')
    mypath = path[0]
mypath



# return a csv file
@st.experimental_memo
@st.cache
def get_data() -> pd.DataFrame:
    # read a csv file
    df_source = pd.read_csv(f"{mypath}src/getaround_delay_filled.csv")
    df=df_source.drop(['rental_id','car_id','previous_ended_rental_id'],axis=1)
    return df

def func_filter(cat_column,selectbox):
    res = df[cat_column] == selectbox
    if selectbox == 'all':
        res = True
#def func_threshold(operation in(>,<,==)):
#        return threshold_less_0 = df[df['delay_at_checkout_in_minutes'] operation 0]
                   
                   
#        for col in pd.unique(df[cat_column]):
#            res = res & (df[cat_column] == col)
    return res

#def func_metric(filter,column):
#    df = get_data()
#    df[filter][columns].
    
df = get_data()
df_source = pd.read_csv(f"{mypath}src/getaround_delay_filled.csv")
df_source_exc = pd.read_csv(f"{mypath}src/get_around_pricing_project_cleaned.csv")
price_per_minute = round(df_source_exc['rental_price_per_day'].mean()/24/60,4)
# dashboard title
st.title("Getaround delay analysis")

### Side bar 
st.sidebar.header("Build dashboards with Streamlit")
col1,_ = st.sidebar.columns(2)
with col1:
    st.sidebar.markdown("""
    * [Key performance indicators](#Key-performance-indicators)
    * [Charts](#charts)
    * [Charts directly built with Streamlit](#simple-bar-chart-built-directly-with-streamlit)
    * [Load and showcase data](#load-and-showcase-data)
""")
## top-level filters
#col3,col4 = st.columns(2)
state_filter = st.sidebar.selectbox("Select the state type", ['all',*pd.unique(df["state"])],index=0)
checkin_filter = st.sidebar.selectbox("Select the checkin type", ['all',*pd.unique(df["checkin_type"])],index=0)
delay_slider = st.sidebar.slider("Select the delay at checkout",min_value=-15000, max_value=15000, value=0, step=1)
time_delta_slider = st.sidebar.slider("Select the time delta type",max_value=10000, value=0, step=1)

st.sidebar.empty()
st.sidebar.write("Made for the certification by Ndangani :sunglasses:")

# creating a single-element container
placeholder = st.empty()
chartholder = st.empty()

# dataframe filter
df_state_filter = df[df["state"] == state_filter]
df_delay_slider = df[df["delay_at_checkout_in_minutes"] == delay_slider]
df_checkin_filter = df[df["checkin_type"] == checkin_filter]
df_time_delta_slider = df[df["time_delta_with_previous_rental_in_minutes"] == time_delta_slider]


# near real-time / live feed simulation
for seconds in range(200):

    #df_delay_filter["age_new"] = df_delay_filter["age"] * np.random.choice(range(1, 5))
    #df_delay_filter["balance_new"] = df_delay_filter["balance"] * np.random.choice(range(1, 5))
    
## set filter when 'all' is selected in a selextbox    


    # creating KPIs
    df_less = df[(df['delay_at_checkout_in_minutes']<delay_slider)&(func_filter("state",state_filter))&(func_filter("checkin_type",checkin_filter))]
    df_more = df[(df['delay_at_checkout_in_minutes']>delay_slider)&(func_filter("state",state_filter))&(func_filter("checkin_type",checkin_filter))]
    df_equal = df[(df['delay_at_checkout_in_minutes']==delay_slider)&(func_filter("state",state_filter))&(func_filter("checkin_type",checkin_filter))]
    
    df_col = df[(df['delay_at_checkout_in_minutes']==delay_slider)&(func_filter("state",state_filter))&(func_filter("checkin_type",checkin_filter))]
    
    negative_delay = df[(df['delay_at_checkout_in_minutes']<delay_slider)&(func_filter("state",state_filter))&(func_filter("checkin_type",checkin_filter))]['delay_at_checkout_in_minutes']
    positive_delay = df[(df['delay_at_checkout_in_minutes']>delay_slider)&(func_filter("state",state_filter))&(func_filter("checkin_type",checkin_filter))]['delay_at_checkout_in_minutes']
    no_delay = df[(df['delay_at_checkout_in_minutes']==delay_slider)&(func_filter("state",state_filter))&(func_filter("checkin_type",checkin_filter))]['delay_at_checkout_in_minutes']

    
    #negative_delay = df[df['delay_at_checkout_in_minutes']<delay_slider]['delay_at_checkout_in_minutes']
    #positive_delay = df[df['delay_at_checkout_in_minutes']>delay_slider]['delay_at_checkout_in_minutes']
    #no_delay = df[df['delay_at_checkout_in_minutes']==delay_slider]['delay_at_checkout_in_minutes']
    total_delay_count = df['delay_at_checkout_in_minutes'].count()
    
    negative_delay_0 = df[df['delay_at_checkout_in_minutes']<0]['delay_at_checkout_in_minutes']
    positive_delay_0 = df[df['delay_at_checkout_in_minutes']>0]['delay_at_checkout_in_minutes']
    no_delay_0 = df[df['delay_at_checkout_in_minutes']==0]['delay_at_checkout_in_minutes']
    
    
    with placeholder.container():
        st.subheader('Key performance indicators')
        
        #st.radio('set delay', ('late','early','in time'), index=0, key='delay_radio',disabled=False, horizontal=True, label_visibility="visible")
        kpdesc,kpDelay,kpIntime,kpEarly = st.columns([1,1,1,1])
        kpdesc.metric(label="kpdesc",label_visibility='hidden',value='')
        kpdesc.write('delayed check-out')
        # fill in those three columns with respective metrics or KPIs
        kpDelay.metric(label=f'more than {delay_slider} minutes',value=f"{positive_delay.count()}")
        kpDelay.metric(label="in percentage",value=f"{round((100*positive_delay.count()/total_delay_count),2)}%")
        #kpDelay.write('mean cumulative minutes of delay')           
        kpIntime.metric(label=f'equal than {delay_slider} minutes',value=f"{no_delay.count()}")
        kpIntime.metric(label="in percentage",value=f"{round((100*no_delay.count()/total_delay_count),2)}%")       
        #kpIntime.write('mean cumulative minutes in time')
        kpEarly.metric(label=f'less than {delay_slider} minutes',value=f"{negative_delay.count()}")
        kpEarly.metric(label="in percentage",value=f"{round((100*negative_delay.count()/total_delay_count),2)}%")
               
        dec,Delay,Intime,Early = st.columns([1,1,1,1])
        #dec.metric(label="",value='')
        dec.write('')
        dec.write('mean cumulative minutes among same category of check-out')
        Delay.metric(label='delay mean',label_visibility='hidden',value=round(positive_delay_0.sum()/positive_delay_0.count(),2))
        Delay.metric(label='delay mean',label_visibility='hidden',value=round(positive_delay_0.sum()/total_delay_count,2))

        dec.write('mean cumulative minutes among all check-out')
        Intime.metric(label='intime mean',label_visibility='hidden',value=0)
        Intime.metric(label='intime mean',label_visibility='hidden',value=0)
        Early.metric(label='early mean',label_visibility='hidden',value=round(negative_delay_0.sum()/negative_delay_0.count(),2))
        Early.metric(label='early mean',value=round(negative_delay_0.sum()/total_delay_count,2))
             
        st.write("")
        st.write("")
        st.write(f"State: {state_filter}, -------------------------------------------------checkin_type: {checkin_filter} ------------------------------------------------delay : {delay_slider}")
        dec,state,chec,other = st.columns([1,1,1,1])
        #dec.metric(label="state and checkin",label_visibility='hidden',value='')
        #dec.metric(label="state and checkin",label_visibility='hidden',value='')
        #state.metric(label='count',value=df_col['state'].count())
        #chec.metric(label='percentage',value=f"{round(100*df_col['state'].count()/df['state'].count(),2)}%")
        
        state.metric(label="average price per minute",value=f'{price_per_minute} $')
        chec.metric(label="average cost per check-out",value=f"{round(price_per_minute *positive_delay_0.sum()/df['delay_at_checkout_in_minutes'].count(),2)} $")
        other.metric(label="average cost per delayed check-out",value=f'{round(price_per_minute *positive_delay_0.sum()/positive_delay_0.count(),2)} $')
#positive_delay_0.sum()/df_source_exc['delay_at_checkout_in_minutes'].count()        
        
    with chartholder.container():
        st.subheader('Charts')
        # create two columns for charts
        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("### First Chart")
            fig = px.density_heatmap(
                data_frame=df_state_filter, y="delay_at_checkout_in_minutes", x="checkin_type"
            )
            st.write(fig)
            
        with fig_col2:
            st.markdown("### Second Chart")
            fig2 = px.histogram(data_frame=df_checkin_filter, x="delay_at_checkout_in_minutes")
            st.write(fig2)
            
        with fig_col1:
            st.line_chart(negative_delay_0)
        with fig_col2:
            st.line_chart(positive_delay_0)
            
        with fig_col1:  st.line_chart(data=df.loc[df['state']=='canceled',:],x="checkin_type",y="delay_at_checkout_in_minutes")
        
        with fig_col2:  st.line_chart(data=df.loc[df['state']=='ended',:],x="checkin_type",y="delay_at_checkout_in_minutes")
        
        with fig_col1:  st.bar_chart(data=df,x="state",y="delay_at_checkout_in_minutes")
        with fig_col2:  st.bar_chart(data=df,x="checkin_type",y="delay_at_checkout_in_minutes")
        
            
        
        
        #count=0
        ## Run the below code if the check is checked
        #if st.checkbst.line_chart(ox(label='Detailed Data View',key=f"raw_data{count}"):
        #    st.markdown("### Detailed Data View")
        #    #st.write(df_source)
        #    st.dataframe(df_source)
        #    count +=1
        time.sleep(1)
