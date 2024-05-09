FROM python
WORKDIR /BrowserHistory/
COPY . .
RUN pip install -r requirements.txt
CMD python -m dateTime