FROM python:slim
RUN useradd microblog
WORKDIR /home/microblog
COPY . .
RUN chown -R microblog:microblog .
RUN chmod +x boot.sh
USER microblog
ENV PATH "$PATH:/home/microblog/.local/bin"
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]