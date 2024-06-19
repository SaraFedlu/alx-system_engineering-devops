# This Puppet manifest corrects a typo in the WordPress code
file_line { 'fix-typo-class-wp-locale':
  ensure => present,
  path   => '/var/www/html/wp-settings.php',
  match  => 'class-wp-locale.phpp',
  line   => 'require_once ABSPATH . WPINC . \'/class-wp-locale.php\';',
  notify => Service['apache2'],
}

# Ensure Apache service is running and manage its state
service { 'apache2':
  ensure => running,
  enable => true,
}
