import pandas as pd
import requests
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

import streamlit as st

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

name, authentication_status, username = authenticator.login('Login', 'main')

@st.cache_data
def load_data(apiUrl):
    """
    Function to load data from an API endpoint and return a pandas DataFrame.

    Args:
    apiUrl (str): The API endpoint URL to retrieve data from.

    Returns:
    Returns a pandas DataFrame containing the retrieved data.
    """

    data = pd.DataFrame()
    try:
        response_json = requests.get(apiUrl, headers={"Authorization": "Bearer topsecretproject"}).json()
        data = pd.json_normalize(response_json['result'])
    except Exception as e:
        print(e)

    return data

if st.session_state["authentication_status"]:

    st.title('🛍️ H&M Analytics')
    st.caption('Explore H&M\'s analytics with our powerful tool! With a range of valuable insights at your fingertips and a variety of filters available, you can quickly find the information you need to make informed decisions.')

    tab1, tab2, tab3 = st.tabs(["🧑‍🤝‍🧑 Customers", "👕 Articles", "🏢 Departments"])

    result = load_data("http://0.0.0.0:8080/api/customers")
    if result.empty:
        st.write("There was an error loading the data.")
    else:
        # Creating customer df
        customer_df = result.drop(columns=['Active.$numberDouble', 'FN.$numberDouble', 'fashion_news_frequency.$numberDouble', 'age.$numberDouble', 'club_member_status.$numberDouble']).rename(columns={'_id.$oid': '_id'})
        customer_df['Active'] = customer_df['Active'].fillna('None')
        customer_df['FN'] = customer_df['FN'].fillna('None')
        filt_customer_df = customer_df.copy()

        # Customer Sidebar Components
        st.sidebar.title("🔍 Filters")
        status_lst = customer_df['club_member_status'].unique()
        fashion_lst = customer_df['fashion_news_frequency'].unique()
        active_lst = customer_df['Active'].unique()
        fn_lst = customer_df['FN'].unique()

        st.sidebar.header("Customer Filters")
        status_filtered_lst = st.sidebar.multiselect(
            label='Club Member Status',
            options= status_lst,
            default= status_lst,
            key="multiselect_status"
        )

        fashion_filtered_lst = st.sidebar.multiselect(
            label='Fashion News Fequency',
            options= fashion_lst,
            default= fashion_lst,
            key="multiselect_fashion"
        )

        active_filtered_lst = st.sidebar.multiselect(
            label='Active',
            options= active_lst,
            default= active_lst,
            key="multiselect_active"
        )

        fn_filtered_lst = st.sidebar.multiselect(
            label='FN',
            options= fn_lst,
            default= fn_lst,
            key="multiselect_fn"
        )

        ages_filtered_lst = st.sidebar.slider(
            'Age', 0, int(customer_df['age'].max()), (0, int(customer_df['age'].max()))
        )

        # Filtering customer df
        filt_customer_df = customer_df.loc[customer_df['club_member_status'].isin(status_filtered_lst) & customer_df['fashion_news_frequency'].isin(fashion_filtered_lst) & customer_df['Active'].isin(active_filtered_lst) & customer_df['FN'].isin(fn_filtered_lst) & (customer_df['age']>=ages_filtered_lst[0]) & (customer_df['age']<=ages_filtered_lst[1]) ] 

        # Creating transaction df
        transaction_df = load_data("http://0.0.0.0:8080/api/transactions")

        # Transactions Sidebar Components
        sales_channel_lst = transaction_df['sales_channel_id'].unique()
        st.sidebar.header("Transactions Filters")
        sales_channel_filtered_lst = st.sidebar.multiselect(
            label='Sales Channnel',
            options= sales_channel_lst,
            default= sales_channel_lst,
            key="multiselect_sales_channel"
        )

        # Filtering transactions df
        filt_transaction_df = transaction_df.loc[transaction_df['sales_channel_id'].isin(sales_channel_filtered_lst) ] 

         # Creating article df
        article_df = load_data("http://0.0.0.0:8080/api/articles")

        # Merging dfs
        merged_df = filt_transaction_df[['customer_id', 'price', 'sales_channel_id']].merge(filt_customer_df[['customer_id', 'club_member_status', 'age']], on='customer_id', how='inner')

        # df for article and department statistics
        tot_sales = filt_transaction_df.merge(filt_customer_df['customer_id'], on="customer_id", how='inner').groupby('article_id')['price'].agg(['count', 'sum']) \
        .merge(article_df[['article_id', 'index_name', 'department_name', 'section_name', 'garment_group_name', 'prod_name', 'graphical_appearance_name', 'colour_group_name']], on='article_id', how='inner') \
        .sort_values(['count'], ascending=False)
        tot_sales = tot_sales.rename(columns={'count': 'Items_Sold', 'sum': 'Revenue'})

        with tab1:  
            st.subheader('📊 Customer Statistics')

            col1, col2, col3, col4 = st.columns(4)
            col1.metric('Customers', len(filt_customer_df))
            col2.metric('Average Age', round(filt_customer_df['age'].mean(), 2))

            active_count = filt_customer_df['Active'].value_counts()
            if active_count.count() > 1:
                col3.metric("% Active", ((active_count[1.0] / len(filt_customer_df['Active'])) * 100).round(2))
            else:
                col3.metric("% Active", '0')

            fn_count = filt_customer_df['FN'].value_counts()
            if fn_count.count() > 1:
                col4.metric("% FN", ((fn_count[1.0] / len(filt_customer_df['FN'])) * 100).round(2))
            else:
                col4.metric("% FN", '0')


            age_group_revenue = merged_df.groupby('age').agg({'price':'sum'}).sort_values(['price'], ascending=False).reset_index().rename(columns={'price': 'MoneySpent'})

            st.write('')
            st.write('')
            st.subheader('💸 Spending by Age')
            st.bar_chart(age_group_revenue.set_index('age')['MoneySpent'])

            st.subheader('🧑‍🤝‍🧑 Customers')
            st.write(filt_customer_df)


        with tab2:  
            st.subheader('🏆 Best-performing Articles')
            top_art_sold = tot_sales.sort_values(['Items_Sold'], ascending=False)[['colour_group_name', 'prod_name']]
            top_art_rev = tot_sales.sort_values(['Revenue'], ascending=False)[['colour_group_name', 'prod_name']]

            # checking if their are values to display   
            if top_art_rev.empty:
                st.metric("Top Selling Article","No article information") 
                st.metric("Top Revenue-Generating Article","No article information") 
            else:
                st.metric("Top Selling Article",top_art_sold['colour_group_name'].iloc[0]+" "+top_art_sold['prod_name'].iloc[0], help="This is the article with the most items sold.") 
                st.metric("Top Revenue-Generating Article",top_art_rev['colour_group_name'].iloc[0]+" "+top_art_rev['prod_name'].iloc[0], help="This is the article that has generated the most revenue.")
            
            st.write('')
            st.write('')
            st.subheader('📈 All Articles')
            st.bar_chart(tot_sales.set_index('prod_name')['Revenue'])


        with tab3:  
            st.subheader('🏆 Best-performing Departments')

            top_dep_sold = tot_sales.groupby('department_name').agg({'Items_Sold': "sum"}).sort_values(['Items_Sold'], ascending=False).reset_index()['department_name']
            top_dep_rev = tot_sales.groupby('department_name').agg({'Revenue': 'sum'}).sort_values(['Revenue'], ascending=False).reset_index()['department_name']

            col5, col6 = st.columns(2)

            # checking if their are values to display
            if top_dep_rev.empty:
                col5.metric("Top Selling Department","No department information") 
                col6.metric("Top Revenue-Generating Department","No department information") 
            else:
                col5.metric("Top Selling Department",top_dep_sold.iloc[0], help="This is the department with the most items sold.") 
                col6.metric("Top Revenue-Generating Department",top_dep_rev.iloc[0], help="This is the department that has generated the most revenue.")

            st.write('')
            st.write('')
            st.subheader('📈 All Departments')
            top_dep_rev_chart = tot_sales.groupby('department_name').agg({'Revenue': 'sum'}).sort_values(['Revenue'], ascending=False).reset_index()
            st.bar_chart(top_dep_rev_chart.set_index('department_name')['Revenue'])

elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')