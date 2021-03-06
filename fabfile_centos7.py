# -*- coding: utf-8 -*-
from fabric.api import sudo, task, cd, put


@task
def install_common():
    # sudo("yum -y install sqlite sqlite-devel")
    sudo("yum -y install curl-devel apr-devel apr-util-devel libffi-devel openssh openssl-devel readline-devel zlib-devel libcurl-devel")
    sudo("yum -y install vim")
    sudo("sudo yum -y install ImageMagick ImageMagick-devel")

    install_git()


@task
def install_git():
    sudo("yum install -y curl-devel expat-devel gettext-devel openssl-devel zlib-devel perl-ExtUtils-MakeMaker")

    with cd("/tmp"):
        sudo("wget https://www.kernel.org/pub/software/scm/git/git-2.9.0.tar.xz")
        sudo("tar xf git-2.9.0.tar.xz")
        with cd("git-2.9.0"):
            sudo("./configure prefix=/usr/local")
            sudo("make all")
            sudo("make install")


@task
def install_mdns():
    sudo("yum -y install avahi nss-mdns")
    sudo("service avahi-daemon start")


@task
def install_ruby():
    """
    rbenvをInstallしてrbenvでrubyをインストールするタスク
    """

    # env
    put("./ruby/rbenv.sh", "/etc/profile.d/", use_sudo=True)

    # rbenv
    with cd("/usr/local"):
        sudo("git clone git://github.com/sstephenson/rbenv.git rbenv", warn_only=True)
        sudo("mkdir rbenv/shims rbenv/versions rbenv/plugins", warn_only=True)
        put("./ruby/default-gems", "/usr/local/rbenv/", use_sudo=True)
        sudo("groupadd rbenv")
        sudo("chgrp -R rbenv rbenv")
        sudo("chmod -R g+rwxXs rbenv")

        # default gems

    # ruby-build
    with cd("/usr/local/rbenv/plugins"):
        sudo("git clone git://github.com/sstephenson/ruby-build.git ruby-build")
        sudo("chgrp -R rbenv ruby-build")
        sudo("chmod -R g+rwxs ruby-build")

        # rbenv-default-gems
        sudo("git clone git://github.com/sstephenson/rbenv-default-gems.git rbenv-default-gems")
        sudo("chgrp -R rbenv rbenv-default-gems")
        sudo("chmod -R g+rwxs rbenv-default-gems")

        # install ruby
        sudo("rbenv install 2.3.1")
        sudo("rbenv global 2.3.1")


@task
def install_rails():
    """
    railsインストール
    """
    # sudo("gem install rails --no-ri --no-doc")
    sudo("gem install rails --no-ri --no-doc --version=\"~>4.2.0\"")


@task
def install_rails5():
    """
    rails 5インストール
    """
    sudo("gem install rails --no-ri --no-doc")


@task
def install_mecab():
    sudo("rpm -ivh http://packages.groonga.org/centos/groonga-release-1.1.0-1.noarch.rpm")
    sudo("yum makecache")
    sudo("yum install -y mecab mecab-ipadic")


# CentOS7用
@task
def install_mysql():
    sudo("yum remove mariadb-libs")
    sudo("rm -rf /var/lib/mysql")
    sudo("yum localinstall http://dev.mysql.com/get/mysql57-community-release-el7-7.noarch.rpm")

    sudo("yum -y install mysql-community-server")
    sudo("yum -y install mysql-devel")
    sudo("systemctl enable mysqld.service")  # centos7
    sudo("systemctl start mysqld.service")   # centos7


@task
def install_nginx():
    sudo("sudo rpm -ivh http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm")
    sudo("sudo yum -y install nginx")
    sudo("chkconfig nginx on")
    sudo("service nginx start")


@task
def install_node():
    sudo("rpm -ivh http://ftp.riken.jp/Linux/fedora/epel/6/x86_64/epel-release-6-8.noarch.rpm")
    sudo("yum -y install nodejs npm --enablerepo=epel")
    sudo("npm install -g bower")


@task
def setup_locale():
    sudo("mv /etc/localtime /etc/localtime.org")
    sudo("ln -s /usr/share/zoneinfo/Asia/Tokyo /etc/localtime")


@task
def install_all():
    # install_common()
    # install_mdns()
    # install_ruby()
    # install_rails()
    install_mecab()
    install_mysql()
    install_nginx()
    install_node()
    setup_locale()
