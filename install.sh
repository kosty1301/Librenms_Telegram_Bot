clear

if ls -l | grep Password_and_token.py
    then
        echo "you already have pass. file, overwrite ?  y/n"
            read overwrite
        if [ "$overwrite" != "y" ]
            then
                exit 1
        fi
fi

echo "# passwords and token"  > Password_and_token.py

echo "Please fingerprint new password:"
    read PASSWORD

echo "Please input your Librenms Token:"
    read LIBRENMS_TOKEN

echo "Please input your Librenms url, like this: 'https://exemple.com/api/v0/'"
    read LIBRENMS_URL

echo "Please input your Telegram Token"
    read TELEGRAM_TOKEN



echo "PASSWORD = '$PASSWORD'"  >> Password_and_token.py
echo "TELEGRAM_TOKEN = '$TELEGRAM_TOKEN'"  >> Password_and_token.py
echo "LIBRENMS_TOKEN = '$LIBRENMS_TOKEN'"  >> Password_and_token.py
echo "LIBRENMS_URL = '$LIBRENMS_URL'" >> Password_and_token.py

clear
echo "Generate settings file is successful"
sleep 2

echo "install requirements ?  y/n"
    read requirements

if [ "$requirements" != "y" ]
    then
        echo "requirements not installing"
    else
        pip install -r requirements.txt
        echo "requirements has been installing"
fi


echo "Make migrations ? y/n"
    read migrations

if [ "$migrations" != "y" ]
    then
        exit 1
    else
        python3 ./models.py
fi


