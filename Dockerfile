WORKDIR /root/MyTgBot

COPY . .

RUN pip3 install --upgrade pip setuptools

RUN pip install -U -r requirements.txt

CMD ["python3","-m","MyTgBot"]
