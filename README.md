Forecasting Service made on Laravel integrated with Vue.js for frontend development. Follow the steps below to clone the repository and set up the project on your local machine.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Step 1: Install PHP 8.3 and Required Extensions](#step-1-install-php-83-and-required-extensions)
3. [Step 2: Install Nginx and PHP-FPM](#step-2-install-nginx-and-php-fpm)
4. [Step 3: Install PostgreSQL](#step-3-install-postgresql)
5. [Step 4: Clone the Repository](#step-4-clone-the-repository)
6. [Step 5: Install Composer Dependencies](#step-5-install-composer-dependencies)
7. [Step 6: Install Node.js and NPM Dependencies](#step-6-install-nodejs-and-npm-dependencies)
8. [Step 7: Configure the Environment](#step-7-configure-the-environment)
9. [Step 8: Compile Assets](#step-8-compile-assets)
10. [Step 9: Run Migrations and Seeders](#step-9-run-migrations-and-seeders)
10. [Step 10: Copy data from Remote server](#step-10-copy-data-from-remote-server)
11. [Step 11: Configure Nginx for Laravel](#step-11-configure-nginx-for-laravel)
12. [Troubleshooting](#troubleshooting)

---

## Prerequisites
Before setting up the project, ensure you have:
- A clean installation of **Ubuntu** (tested on 20.04/22.04).
- Access to a terminal or SSH.
- Basic knowledge of Linux commands.

---

## Step 1: Install PHP 8.3 and Required Extensions
Add the PHP 8.3 repository and install PHP along with required extensions:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:ondrej/php -y
sudo apt update
sudo apt install php8.3 php8.3-cli php8.3-fpm php8.3-pgsql php8.3-mbstring php8.3-xml php8.3-bcmath php8.3-zip php8.3-curl -y
```

Verify the PHP version:
```bash
php -v
```

---

## Step 2: Install Nginx and PHP-FPM
Install Nginx and PHP-FPM:
```bash
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

Ensure PHP-FPM is running:
```bash
sudo systemctl start php8.3-fpm
sudo systemctl enable php8.3-fpm
```

---

## Step 3: Install PostgreSQL
Install PostgreSQL and create a database for the project:
```bash
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

Switch to the `postgres` user and create a database:
```bash
sudo -i -u postgres
createdb laravel_project_db
createuser --pwprompt laravel_user
```

Grant privileges to the user:
```sql
psql
GRANT ALL PRIVILEGES ON DATABASE laravel_project_db TO laravel_user;
\q
exit
```

---

## Step 4: Clone the Repository
Navigate into the Nginx directory:
```bash
cd /var/www/html
```

Clone the project repository from GitHub using the following command:
```bash
sudo git clone https://git.iszf.irk.ru/diegon/forecasting-service.git
```

Navigate into the project directory:
```bash
cd forecasting-service
```

Change rights to Nginx user:
```bash
chown -R www-data:www-data .
```

---

## Step 5: Install Composer Dependencies
Install Composer if not already installed:
```bash
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
```

Install PHP dependencies:
```bash
composer install
```

---

## Step 6: Install Node.js and NPM Dependencies
Install Node.js and NPM:
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y
```

Install JavaScript dependencies:
```bash
npm install
```

---

## Step 7: Configure the Environment
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```

Update the `.env` file with your environment-specific settings, such as database credentials:
```env
DB_CONNECTION=pgsql
DB_HOST=127.0.0.1
DB_PORT=5432
DB_DATABASE=your_database_name
DB_USERNAME=your_database_user
DB_PASSWORD=your_database_password

REMOTE_DB_CONNECTION=pgsql
REMOTE_DB_HOST=10.0.5.78
REMOTE_DB_PORT=5432
REMOTE_DB_DATABASE=remote_database_name
REMOTE_DB_USERNAME=remote_database_user
REMOTE_DB_PASSWORD=remote_database_password

```

Generate an application key:
```bash
php artisan key:generate
```

---

## Step 8: Compile Assets
Compile the frontend assets using Vite:
```bash
npm run dev
```

For production:
```bash
npm run build
```

---

## Step 9: Run Migrations and Seeders
Run the database migrations:
```bash
php artisan migrate
```

If seeders are included, populate the database:
```bash
php artisan db:seed
```

---

## Step 10: Copy data from Remote server
Make sure your script is executable:
```bash
chmod +x /path/to/project/copy_forecast.sh
```

Run the script manually to ensure it works as expected and copy data in first time:
```bash
/path/to/project/copy_forecast.sh
```

### **Schedule the Script with Cron**
Add a cron job to run the script at your desired interval. For example, to run the script every day at 2 AM:
```cron
0 2 * * * /path/to/project/copy_forecast.sh >> /path/to/project/copy_forecast.log 2>&1
```

---


## Step 11: Configure Nginx for Laravel
Create an Nginx configuration file for the project:
```bash
sudo nano /etc/nginx/sites-available/laravel_project
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/your-repo-name/public;

    index index.php index.html;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
    }

    location ~ /\.ht {
        deny all;
    }
}
```

Enable the site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/laravel_project /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Troubleshooting
### Common Issues and Solutions
1. **PHP Version Not Found**:
   - Ensure the `ondrej/php` PPA is added correctly and PHP 8.3 is installed.
   - Use `update-alternatives` to set PHP 8.3 as the default version.

2. **Nginx 502 Bad Gateway**:
   - Check if PHP-FPM is running: `systemctl status php8.3-fpm`.
   - Verify the socket path in the Nginx configuration matches the PHP-FPM configuration.

3. **Database Connection Errors**:
   - Double-check `.env` file credentials.
   - Ensure PostgreSQL is running and the database exists.

---

## Usefull links

For more information, refer to the official documentation:
- [Laravel Documentation](https://laravel.com/docs)
- [Vue.js Documentation](https://vuejs.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

