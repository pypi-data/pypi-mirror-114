FROM fedora:latest

VOLUME /opt/robotframework/tests

# Basic OS and Phyton dependencies
RUN dnf upgrade -y && dnf update -y
RUN dnf install -y python39 pip docker wget
RUN dnf module install -y nodejs:12
# Database dependencies PostgreSQL
RUN dnf install -y libpq-devel
# Database dependencies MySQL
RUN wget https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python3-8.0.25-1.fc34.x86_64.rpm
RUN dnf localinstall -y mysql-connector-python3-8.0.25-1.fc34.x86_64.rpm
RUN wget https://dev.mysql.com/get/Downloads/Connector-ODBC/8.0/mysql-connector-odbc-8.0.25-1.fc34.x86_64.rpm
RUN dnf localinstall -y mysql-connector-odbc-8.0.25-1.fc34.x86_64.rpm
RUN wget https://dev.mysql.com/get/Downloads/Connector-ODBC/8.0/mysql-connector-odbc-setup-8.0.25-1.fc34.x86_64.rpm
RUN dnf localinstall -y mysql-connector-odbc-setup-8.0.25-1.fc34.x86_64.rpm
# Database dependencies Oracle Client
RUN dnf install -y libaio libnsl
RUN wget https://download.oracle.com/otn_software/linux/instantclient/19600/oracle-instantclient19.6-basic-19.6.0.0.0-1.x86_64.rpm
RUN dnf localinstall -y oracle-instantclient19.6-basic-19.6.0.0.0-1.x86_64.rpm
# Prior SDK and Python setup dependencies
RUN pip install docker setuptools wheel twine
# FTSA installation for production environment
RUN pip install ftsa-tjpb && ftsa install
# FTSA installation for tests environment
#RUN pip install -i https://test.pypi.org/simple/ ftsa-tjpb==x.y.z.w
#RUN ftsa install
#RUN pip install -i https://test.pypi.org/simple/ ftsa-tjpb-core==x.y.z.w

WORKDIR /opt/robotframework/tests
