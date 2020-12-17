FROM python:3.7
RUN pip3 install python-telegram-bot
RUN pip3 install numpy
RUN pip3 install Pillow
RUN mkdir /skeleton-bot
ADD . /skeleton-bot
WORKDIR /skeleton-bot
CMD python main.py
