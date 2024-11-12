FROM alpine:latest



# 更新安装包并安装依赖
RUN apk update && apk upgrade && \
    apk add --no-cache python3=3.12.6-r0 py3-pip

RUN ln -sf /usr/bin/python3 /usr/bin/python

RUN python --version

RUN pip --version
# 设置工作目录

WORKDIR /home/www

# 复制当前目录中的应用程序文件到容器中的 /app 目录
COPY . /home/www


RUN python -m venv env
RUN . env/bin/activate


# 更新 pip 并安装依赖
RUN pip install --upgrade pip
RUN pip install -r requirements.txt



# 暴露 FastAPI 应用程序的端口
EXPOSE 8000


RUN echo '陈火火'

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]