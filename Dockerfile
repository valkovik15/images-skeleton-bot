FROM python:3.7
RUN pip3 install python-telegram-bot
RUN pip3 install numpy
RUN pip3 install Pillow
RUN pip3 install scikit-image
RUN mkdir /skeleton-bot
ADD . /skeleton-bot
WORKDIR /skeleton-bot/skeleton-bot
CMD python main.py
