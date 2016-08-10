# -*- coding: utf-8 -*-
from fabric.api import sudo, task, cd, put


@task
def install_common():
    # sudo("yum -y install sqlite sqlite-devel")
    sudo("yum -y install curl-devel apr-devel apr-util-devel libffi-devel openssh openssl-devel readline-devel zlib-devel libcurl-devel")
    sudo("yum -y install git vim")


@task
def install_mdns():
    sudo("yum -y install avahi nss-mdns")
    sudo("service messagebus start")  # centos6
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
def install_node():
    pass


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
    sudo("yum install -y nginx")


@task
def install_rails_template():
    sudo("mkdir -p /var/www/rails", warn_only=True)
    put("./rails4_template.rb", "/var/www/rails/rails4_template.rb", use_sudo=True)
    with cd("/var/www/rails"):
        sudo("rails new template_dummy -d mysql -m rails4_template.rb")
