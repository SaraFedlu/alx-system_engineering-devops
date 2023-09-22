# this Puppet manifest is to kill a process named killmen killmenowow
exec { 'pkill killmenow':
  path => '/bin/',
}
