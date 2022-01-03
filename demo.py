from numpy import insert
import streamlit as st
import pandas as pd

st.title('Convert Excel -> SQL')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
  
    xl = pd.read_csv(uploaded_file)
    xl.dropna()
    xl.drop(xl.filter(regex="Unnamed"),axis=1, inplace=True)


    viewExcel = st.checkbox('Show Excel File')

    if viewExcel:
        st.write(xl)


    oneGO = st.checkbox('Insert all rows in one GO')

    #st.text(len(xl))

    #st.text(''.join(str(list(xl.values.tolist()[0]))))

    st.text(str(len(list(xl.columns)))+' Columns Detected : ' + ', '.join(xl.columns))

    tableName = st.text_input('Enter Table Name ', 'TempTableCase#########')
    #st.write('Table Name :- ', tableName)

    op1 = '/*  CREATE TABLE  */\nCREATE TABLE ' + tableName + '('

    op2='\n'
    for col in xl.columns:
        op2 += col + ' INT,\n' if str(xl[col][0]).isdigit() else col + ' VARCHAR(' + str(len(max(xl[col]))) + '),' + '\n'


    output = st.text_area('Create Table Code : '
        ,op1+op2[:-2] + '\n);'
        ,height=len(xl.columns) + 2
        ,help = 'Code to Create Table')
    

    if oneGO:
        op3 = '/*  INSERT ALL ROWS  */\nINSERT INTO ' + tableName + '\nVALUES\n'

        op4 = ''
        for i in range(len(xl)):
            op4 += '(' + ''.join(str(list(xl.values.tolist()[i])))[1:-1] + '),\n'

        output = st.text_area('Insert all rows in one GO : '
            ,op3+op4+');'
            ,height=len(xl.columns) + 2
            ,help = 'Code to Insert into Table')


    else:
        ins = ''
        for i in range(len(xl)):
            ins += '/*  INSERT QUERY ' + str(i+1) + '  */\n' \
                + 'INSERT INTO ' + tableName + ' (' + ', '.join(xl.columns) \
                + ') \nVALUES(' + '\n' \
                + ''.join(str(list(xl.values.tolist()[i])))[1:-1] + '\n);\n'



        output2 = st.text_area('Insert Data Code : '
            ,ins
            ,height=len(xl.columns) + 2
            ,help = 'Code to insert into Table')