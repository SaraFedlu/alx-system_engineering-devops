# This Puppet manifest configures Nginx and system settings to handle more open files

# Install Nginx
package { 'nginx':
  ensure => installed,
}

# Configure system limits for file descriptors
file_line { 'set soft nofile limit':
  ensure => present,
  path   => '/etc/security/limits.conf',
  line   => '* soft nofile 65536',
}

file_line { 'set hard nofile limit':
  ensure => present,
  path   => '/etc/security/limits.conf',
  line   => '* hard nofile 65536',
}

file_line { 'set www-data soft nofile limit':
  ensure => present,
  path   => '/etc/security/limits.conf',
  line   => 'www-data soft nofile 65536',
}

file_line { 'set www-data hard nofile limit':
  ensure => present,
  path   => '/etc/security/limits.conf',
  line   => 'www-data hard nofile 65536',
}

file_line { 'pam_limits for common-session':
  ensure => present,
  path   => '/etc/pam.d/common-session',
  line   => 'session required pam_limits.so',
}

file_line { 'pam_limits for common-session-noninteractive':
  ensure => present,
  path   => '/etc/pam.d/common-session-noninteractive',
  line   => 'session required pam_limits.so',
}

file_line { 'sysctl file-max setting':
  ensure => present,
  path   => '/etc/sysctl.conf',
  line   => 'fs.file-max = 2097152',
  notify => Exec['reload-sysctl'],
}

exec { 'reload-sysctl':
  command     => '/sbin/sysctl -p',
  refreshonly => true,
}

# Content for /etc/nginx/nginx.conf
file { '/etc/nginx/nginx.conf':
  ensure  => file,
  content => "
user  www-data;
worker_processes  auto;
worker_rlimit_nofile 65536;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '\\\$remote_addr - \\\$remote_user [\\\$time_local] \"\\\$request\" '
                      '\\\$status \\\$body_bytes_sent \"\\\$http_referer\" '
                      '\"\\\$http_user_agent\" \"\\\$http_x_forwarded_for\"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    keepalive_timeout  65;

    include /etc/nginx/conf.d/*.conf;
}
  ",
  notify  => Service['nginx'],
  require => Package['nginx'],
}

# Ensure Nginx service is running and enabled
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/nginx.conf'],
  require   => Package['nginx'],
}
