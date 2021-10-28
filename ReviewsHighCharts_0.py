import justpy as jp

def app():
    wp = jp.QuasarPage() 
    h1 = jp.QDiv(a=wp,text="Analysis of Course Reviews", 
        classes="text-h4 q-pa-md text-center text-weight-bold") 
    p1 = jp.QDiv(a=wp,text="The graphs below represent course review analysis: ",
        classes="q-pl-md") 
    return wp 

jp.justpy(app)