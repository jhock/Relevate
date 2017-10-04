sudo yum install fontconfig freetype freetype-devel fontconfig-devel libstdc++
sudo wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.8-linux-x86_64.tar.bz2
sudo mkdir -p /opt/phantomjs
bzip2 -d phantomjs-1.9.8-linux-x86_64.tar.bz2
sudo tar -xvf phantomjs-1.9.8-linux-x86_64.tar --directory /opt/phantomjs/ --strip-components 1
sudo ln -s /opt/phantomjs/bin/phantomjs /usr/bin/phantomjs