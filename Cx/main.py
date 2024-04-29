import streamlit as st
from streamlit_option_menu import option_menu
import database as db
import validations as val
import time
import send_mail as sm
import hasher as hs
import base64
import backend as be
import coordinates as cr

#---------------------------------------------------
# page config settings:

page_title="Climate Xplorer"
page_icon=""
layout="centered"

st.set_page_config(page_title=page_title,page_icon=page_icon,layout=layout)
st.title(page_title+" "+page_icon)

#--------------------------------------------------

weather_conditions = {
    'thunderstorm with light rain': 'https://www.weather.gov/safety/thunderstorm-200',
    'thunderstorm with rain': 'https://www.weather.gov/safety/thunderstorm-201',
    'thunderstorm with heavy rain': 'https://www.weather.gov/safety/thunderstorm-202',
    'light thunderstorm': 'https://www.weather.gov/safety/thunderstorm-210',
    'thunderstorm': 'https://www.weather.gov/safety/thunderstorm-211',
    'heavy thunderstorm': 'https://www.weather.gov/safety/thunderstorm-212',
    'ragged thunderstorm': 'https://www.weather.gov/safety/thunderstorm-221',
    'thunderstorm with light drizzle': 'https://www.weather.gov/safety/thunderstorm-230',
    'thunderstorm with drizzle': 'https://www.weather.gov/safety/thunderstorm-231',
    'thunderstorm with heavy drizzle': 'https://www.weather.gov/safety/thunderstorm-232',
    'light intensity drizzle': 'https://www.weather.gov/safety/drizzle-300',
    'drizzle': 'https://www.weather.gov/safety/drizzle-301',
    'heavy intensity drizzle': 'https://www.weather.gov/safety/drizzle-302',
    'light intensity drizzle rain': 'https://www.weather.gov/safety/drizzle-310',
    'drizzle rain': 'https://www.weather.gov/safety/drizzle-311',
    'heavy intensity drizzle rain': 'https://www.weather.gov/safety/drizzle-312',
    'shower rain and drizzle': 'https://www.weather.gov/safety/drizzle-313',
    'heavy shower rain and drizzle': 'https://www.weather.gov/safety/drizzle-314',
    'shower drizzle': 'https://www.weather.gov/safety/drizzle-321',
    'light rain': 'https://www.weather.gov/safety/rain-500',
    'moderate rain': 'https://www.weather.gov/safety/rain-501',
    'heavy intensity rain': 'https://www.weather.gov/safety/rain-502',
    'very heavy rain': 'https://www.weather.gov/safety/rain-503',
    'extreme rain': 'https://www.weather.gov/safety/rain-504',
    'freezing rain': 'https://www.weather.gov/safety/rain-511',
    'light intensity shower rain': 'https://www.weather.gov/safety/rain-520',
    'shower rain': 'https://www.weather.gov/safety/rain-521',
    'heavy intensity shower rain': 'https://www.weather.gov/safety/rain-522',
    'ragged shower rain': 'https://www.weather.gov/safety/rain-531',
    'light snow': 'https://www.weather.gov/safety/snow-600',
    'snow': 'https://www.weather.gov/safety/snow-601',
    'heavy snow': 'https://www.weather.gov/safety/snow-602',
    'sleet': 'https://www.weather.gov/safety/snow-611',
    'light shower sleet': 'https://www.weather.gov/safety/snow-612',
    'shower sleet': 'https://www.weather.gov/safety/snow-613',
    'light rain and snow': 'https://www.weather.gov/safety/snow-615',
    'rain and snow': 'https://www.weather.gov/safety/snow-616',
    'light shower snow': 'https://www.weather.gov/safety/snow-620',
    'shower snow': 'https://www.weather.gov/safety/snow-621',
    'heavy shower snow': 'https://www.weather.gov/safety/snow-622',
    'mist': 'https://www.weather.gov/safety/atmosphere-701',
    'smoke': 'https://www.weather.gov/safety/atmosphere-711',
    'haze': 'https://images.pexels.com/photos/39811/pexels-photo-39811.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    'sand/dust whirls': 'https://www.weather.gov/safety/atmosphere-731',
    'fog': 'https://www.weather.gov/safety/atmosphere-741',
    'sand': 'https://www.weather.gov/safety/atmosphere-751',
    'dust': 'https://www.weather.gov/safety/atmosphere-761',
    'volcanic ash': 'https://www.weather.gov/safety/atmosphere-762',
    'squalls': 'https://www.weather.gov/safety/atmosphere-771',
    'tornado': 'https://www.weather.gov/safety/atmosphere-781',
    'clear sky': 'https://images.unsplash.com/photo-1601297183305-6df142704ea2?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
    'few clouds: 11-25%': 'https://www.weather.gov/safety/clouds-801',
    'scattered clouds: 25-50%': 'https://www.weather.gov/safety/clouds-802',
    'broken clouds: 51-84%': 'https://www.weather.gov/safety/clouds-803',
    'overcast clouds: 85-100%': 'https://www.weather.gov/safety/clouds-804'
}


#--------------------------------------------------
#hide the header and footer     

hide_ele="""
        <style>
        #Mainmenu {visibility:hidden;}
        footer {visibility:hidden;}
        header {visibility:hidden;}
        </style>
        """
st.markdown(hide_ele,unsafe_allow_html=True)


def set_default_bg(url):
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("{url}");
             background-size: cover;
             opacity: 0.8; 
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
set_default_bg("https://images.unsplash.com/photo-1618886487325-f665032b6352?q=80&w=1964&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
def set_bg_hack_url(current_weather):
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("{weather_conditions[current_weather]}");
             background-size: cover;
             opacity: 0.8; 
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
curlogin=""
otp=""

def log_sign():
    selected=option_menu(
        menu_title=None,
        options=["Login","Signup","Admin"],
        icons=["bi bi-file-lock-fill","bi bi-pencil-square","bi bi-people"],
        orientation="horizontal"
    )
    global submit
    if(selected=="Login"):
        tab1,tab2=st.tabs(["Login","Forgot Password"])
        with tab1:
            with st.form("Login",clear_on_submit=True):
                st.header("Login")
                username=st.text_input("Email")
                password=st.text_input("Password",type="password")
                submit=st.form_submit_button()
                if(submit):
                    if(username=="" or password==""):
                        st.warning("Enter your login credentials")
                    else:
                        password=hs.hasher(password)
                        if(db.authenticate(username,password)):
                            st.session_state["curlogin"]=username
                            st.session_state["key"]="main"
                            st.experimental_rerun()
                        else:
                            st.error("Please check your username / password ")
        with tab2:
            with st.form("Forgot Password",clear_on_submit=True):
                st.header("Forgot Password")
                email=st.text_input("Email")
                submit=st.form_submit_button()
                if(submit):
                    if(email==""):
                        st.warning("Enter your email")
                    elif(not db.emailexists(email)):
                        st.warning("email not found")
                    else:
                        otp=sm.forgot_password(email)
                        db.forgot_pass(email,otp)
                        st.success("Check your email for password reset instructions!.")
                
    elif(selected=="Signup"):
         with st.form("Sign Up",clear_on_submit=False):
            st.header("Sign Up")
            email=st.text_input("Enter your email")
            number=st.text_input("Enter your Mobile Number")
            password=st.text_input("Enter your password",type="password")
            submit=st.form_submit_button()
            if(submit):
                dev=db.fetch_all_users()
                emails=[]
                numbers=[]
                for user in dev:
                    emails.append(user["email"])
                    numbers.append(user["number"])
                var=True
                if(val.validate_email(email)==False):
                    st.error("Enter email in a valid format like 'yourname@srmap.edu.in'")
                elif(email in emails):
                    st.error("email already exists!\nTry with another email !")
                elif(val.validate_mobile(number)==False):
                    st.error("Please Check your mobile Number")
                elif(number in numbers):
                    st.error("Phone number already exists\nTry with another number")
                elif(val.validate_password(password)==False):
                    st.error("Password must be between 6-20 characters in length and must have at least one Uppercase Letter , Lowercase letter , numeric character and A Special Symbol(#,@,$,%,^,&,+,=)")
                elif(var):
                    password=hs.hasher(password)
                    db.insert_user(email,password,number)
                    st.success("Signed Up Successfully....Redirecting!!")
                    time.sleep(2)
                    st.session_state["curlogin"]=email
                    st.session_state["key"]="main"
                    st.experimental_rerun()
    elif(selected=="Admin"):
        with st.form("Admin Login",clear_on_submit=True):
            st.header("Admin Login")
            username=st.text_input("Username")
            password=st.text_input("Password",type="password")
            submit=st.form_submit_button()
            if(submit):
                if(username=="" or password==""):
                    st.warning("Enter your login credentials")
                else:
                    if(db.ad_authenticate(username,password)):
                        st.session_state["curlogin"]=username
                        st.session_state["key"]="adminmain"
                        st.experimental_rerun()
                    else:
                        st.error("Please check your username / password ")
            

def main():
    city_name=st.text_input("Enter Your city name : ")
    weather_data=be.get_weather_data(city_name)
    if(weather_data):
        set_bg_hack_url(weather_data['weather'][0]['description'])
    if(city_name):
        wo=option_menu(
            menu_title=None,
            options=["Live Data","Historical Data","Forecast"],
            icons=["bi-bullseye","bi-database"," bi-graph-up-arrow"],
            orientation="horizontal"
        )
        if(wo=="Live Data"):
            if(weather_data):
                st.write("Weather in", city_name)
                st.write("Temperature:", weather_data['main']['temp'], "°C")
                st.write("Description:", weather_data['weather'][0]['description'])
                st.write("Humidity:", weather_data['main']['humidity'], "%")
                st.write("Wind Speed:", weather_data['wind']['speed'], "m/s")
            else:
                st.error("Kindly Double check the City Name")

        elif(wo=="Historical Data"):
            lat,lon=cr.get_coordinates(city_name)
            weather_data=be.get_historical_weather(lat,lon) 
            if(weather_data):
                st.dataframe(weather_data)
            else:
                st.error("Kindly Double check the City Name")
        else:
            lat,lon=cr.get_coordinates(city_name)
            weather_data=be.get_forecast(lat,lon)
            if(weather_data):
                st.dataframe(weather_data)
            else:
                st.error("Kindly Double check the City Name")

def adminmain():
    op=option_menu(
        menu_title=None,
            options=["Password Change","Delete User"],
            icons=["bi-shield-lock-fill","bi-trash-fill"],
            orientation="horizontal"
    )
    if(op=="Password Change"):
        with st.form("Password Change",clear_on_submit=False):
            st.header("Update Details")
            email=st.text_input("Enter your email")
            number=st.text_input("Enter your Mobile Number")
            password=st.text_input("Enter your password",type="password")
            submit=st.form_submit_button()
            if(submit):
                var=True
                if(val.validate_email(email)==False):
                        st.error("Enter email in a valid format like 'yourname@srmap.edu.in'")
                elif(val.validate_mobile(number)==False):
                        st.error("Please Check your mobile Number")
                elif(val.validate_password(password)==False):
                        st.error("Password must be between 6-20 characters in length and must have at least one Uppercase Letter , Lowercase letter , numeric character and A Special Symbol(#,@,$,%,^,&,+,=)")
                elif(var):
                    if(db.emailexists(email)):
                        password=hs.hasher(password)
                        db.update_user(email,password,number)
                        st.success("Database Updated Successfully")
                    else:
                        st.error("No account found with the email address")
    else:
        with st.form("Delete Acc",clear_on_submit=True):
            st.header("Delete Account")
            email=st.text_input("Enter your email")
            submit=st.form_submit_button("Submit")
            if(submit):
                if(db.emailexists(email)):
                    db.delete_user(email)
                    st.success("User Account Deleted Successfully")
                else:
                    st.error("No Account found with the email address")

if "key" not in st.session_state:

    st.session_state["key"] = "log_sign"

if st.session_state["key"] == "log_sign":
    log_sign()

elif st.session_state["key"] == "main":
    main()

elif st.session_state["key"] == "adminmain":
    adminmain()