# Ensure the directory for Puppet manifests exists
file { '/etc/puppet/manifests':
  ensure => directory,
}

# Create the manifest to fix the typo in WordPress
file { '/etc/puppet/manifests/fix-wp-locale.pp':
  ensure  => file,
  content => "exec { 'fix-typo-class-wp-locale':
    command => 'sed -i \"s/class-wp-locale.phpp/class-wp-locale.php/\" /var/www/html/wp-settings.php',
    path    => ['/bin', '/usr/bin', '/sbin', '/usr/sbin'],
  }",
}

# Apply the manifest file to fix the typo
exec { 'apply-file-line':
  command => 'puppet apply /etc/puppet/manifests/fix-wp-locale.pp',
  path    => ['/bin', '/usr/bin', '/sbin', '/usr/sbin'],
  notify  => Service['apache2'],
  require => File['/etc/puppet/manifests/fix-wp-locale.pp'],
}

# Ensure Apache service is running and manage its state
service { 'apache2':
  ensure  => running,
  enable  => true,
  require => Exec['apply-file-line'],
}
