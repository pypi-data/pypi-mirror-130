create table if not exists totp (
    id int not null auto_increment primary key
  , email varchar(120)
  , secret_key varchar(32)
);
create index idx_totp_authenticator_email on totp (email);
create table if not exists last_sign_in (
    id int not null auto_increment primary key
  , email varchar(120)
  , ip_address varchar(64)
  , last_sign_in datetime default current_timestamp
);
create index idx_totp_authenticator_email on last_sign_in (email);
create index idx_totp_authenticator_email_and_ip on last_sign_in (email, ip_address);

create table if not exists ldap_settings (
    id int not null auto_increment primary key
  , domain varchar(120)
  , servers varchar(255)
  , search_base varchar(120)
);
create index idx_ldap_settings_domain on ldap_settings (domain);


