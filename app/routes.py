from datetime import datetime, timezone
from functools import wraps
from flask import jsonify, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash

from app import app, mongo
from app.services.storage import save_upload


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin' not in session:
            flash('Please log in as admin.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


def utc_now():
    return datetime.now(timezone.utc)


@app.route('/')
def home():
    notices = list(mongo.db.notices.find().sort('created_at', -1))
    contacts = list(mongo.db.contacts.find().sort('name', 1))
    mandi_rates = list(mongo.db.mandi_rates.find().sort('updated_at', -1).limit(8))
    works = list(mongo.db.works.find().sort('created_at', -1).limit(3))
    schemes = list(mongo.db.schemes.find().sort('created_at', -1).limit(5))
    jobs = list(mongo.db.jobs.find().sort('created_at', -1).limit(5))
    businesses = list(mongo.db.businesses.find({'approved': True}).sort('created_at', -1).limit(6))
    grievances = list(mongo.db.grievances.find().sort('created_at', -1).limit(5))
    return render_template(
        'index.html',
        notices=notices,
        contacts=contacts,
        mandi_rates=mandi_rates,
        works=works,
        schemes=schemes,
        jobs=jobs,
        businesses=businesses,
        grievances=grievances,
    )


@app.route('/krishi-mitra')
def krishi_mitra():
    mandi_rates = list(mongo.db.mandi_rates.find().sort('updated_at', -1).limit(10))
    return render_template('krishi_mitra.html', mandi_rates=mandi_rates)


@app.route('/digital-panchayat')
def digital_panchayat():
    works = list(mongo.db.works.find().sort('created_at', -1))
    return render_template('digital_panchayat.html', works=works)


@app.route('/sarkari-seva')
def sarkari_seva():
    schemes = list(mongo.db.schemes.find().sort('created_at', -1))
    return render_template('sarkari_seva.html', schemes=schemes)


@app.route('/yuva-rojgar')
def yuva_rojgar():
    jobs = list(mongo.db.jobs.find().sort('created_at', -1))
    return render_template('yuva_rojgar.html', jobs=jobs)


@app.route('/bazaar')
def bazaar():
    businesses = list(mongo.db.businesses.find({'approved': True}).sort('created_at', -1))
    return render_template('bazaar.html', businesses=businesses)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        admin = mongo.db.admins.find_one({'username': username})
        if admin and check_password_hash(admin.get('password', ''), password):
            session['admin'] = admin['username']
            flash('Admin login successful.', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin credentials.', 'danger')
    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_login'))


@app.route('/admin')
@admin_required
def admin_dashboard():
    grievance_count = mongo.db.grievances.count_documents({})
    notice_count = mongo.db.notices.count_documents({})
    pending_count = mongo.db.businesses.count_documents({'approved': False})
    works = list(mongo.db.works.find().sort('created_at', -1))
    schemes = list(mongo.db.schemes.find().sort('created_at', -1))
    jobs = list(mongo.db.jobs.find().sort('created_at', -1))
    businesses = list(mongo.db.businesses.find().sort('created_at', -1))
    grievances = list(mongo.db.grievances.find().sort('created_at', -1))
    contacts = list(mongo.db.contacts.find().sort('created_at', -1))
    mandi_rates = list(mongo.db.mandi_rates.find().sort('updated_at', -1))
    notices = list(mongo.db.notices.find().sort('created_at', -1))
    return render_template(
        'admin_dashboard.html',
        grievance_count=grievance_count,
        notice_count=notice_count,
        pending_count=pending_count,
        works=works,
        schemes=schemes,
        jobs=jobs,
        businesses=businesses,
        grievances=grievances,
        contacts=contacts,
        mandi_rates=mandi_rates,
        notices=notices,
    )


@app.route('/api/notices', methods=['GET', 'POST'])
@admin_required
def notices_api():
    if request.method == 'POST':
        payload = {
            'title': request.form.get('title'),
            'body': request.form.get('body'),
            'created_at': utc_now()
        }
        mongo.db.notices.insert_one(payload)
        return redirect(url_for('admin_dashboard'))
    notices = list(mongo.db.notices.find().sort('created_at', -1))
    return jsonify(notices)


@app.route('/api/notices/<notice_id>', methods=['DELETE'])
@admin_required
def delete_notice(notice_id):
    mongo.db.notices.delete_one({'_id': notice_id})
    return jsonify({'status': 'deleted'})


@app.route('/api/grievances', methods=['GET', 'POST'])
def grievances_api():
    if request.method == 'POST':
        payload = {
            'name': request.form.get('name'),
            'phone': request.form.get('phone'),
            'subject': request.form.get('subject'),
            'description': request.form.get('description'),
            'status': 'new',
            'created_at': utc_now()
        }
        mongo.db.grievances.insert_one(payload)
        flash('Grievance submitted successfully.', 'success')
        return redirect(url_for('home'))
    grievances = list(mongo.db.grievances.find().sort('created_at', -1))
    return jsonify(grievances)


@app.route('/api/mandi-rates', methods=['GET', 'POST'])
@admin_required
def mandi_rates_api():
    if request.method == 'POST':
        payload = {
            'crop': request.form.get('crop'),
            'price': request.form.get('price'),
            'unit': request.form.get('unit', 'quintal'),
            'updated_at': utc_now()
        }
        mongo.db.mandi_rates.insert_one(payload)
        return redirect(url_for('admin_dashboard'))
    rates = list(mongo.db.mandi_rates.find().sort('updated_at', -1))
    return jsonify(rates)


@app.route('/api/businesses', methods=['GET', 'POST'])
@admin_required
def businesses_api():
    if request.method == 'POST':
        payload = {
            'name': request.form.get('name'),
            'category': request.form.get('category'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address'),
            'approved': False,
            'created_at': utc_now()
        }
        mongo.db.businesses.insert_one(payload)
        return redirect(url_for('admin_dashboard'))
    businesses = list(mongo.db.businesses.find().sort('created_at', -1))
    return jsonify(businesses)


@app.route('/api/businesses/<business_id>/approve', methods=['POST'])
@admin_required
def approve_business(business_id):
    mongo.db.businesses.update_one({'_id': business_id}, {'$set': {'approved': True}})
    return jsonify({'status': 'approved'})


@app.route('/api/works', methods=['GET', 'POST'])
@admin_required
def works_api():
    if request.method == 'POST':
        image_path = save_upload(request.files.get('image'), app.config['UPLOAD_FOLDER'])
        payload = {
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'budget_status': request.form.get('budget_status'),
            'image': image_path,
            'created_at': utc_now()
        }
        mongo.db.works.insert_one(payload)
        return redirect(url_for('admin_dashboard'))
    works = list(mongo.db.works.find().sort('created_at', -1))
    return jsonify(works)


@app.route('/api/schemes', methods=['GET', 'POST'])
@admin_required
def schemes_api():
    if request.method == 'POST':
        payload = {
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'link': request.form.get('link'),
            'created_at': utc_now()
        }
        mongo.db.schemes.insert_one(payload)
        return redirect(url_for('admin_dashboard'))
    schemes = list(mongo.db.schemes.find().sort('created_at', -1))
    return jsonify(schemes)


@app.route('/api/jobs', methods=['GET', 'POST'])
@admin_required
def jobs_api():
    if request.method == 'POST':
        payload = {
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'link': request.form.get('link'),
            'created_at': utc_now()
        }
        mongo.db.jobs.insert_one(payload)
        return redirect(url_for('admin_dashboard'))
    jobs = list(mongo.db.jobs.find().sort('created_at', -1))
    return jsonify(jobs)


@app.route('/api/contacts', methods=['GET', 'POST'])
@admin_required
def contacts_api():
    if request.method == 'POST':
        payload = {
            'name': request.form.get('name'),
            'phone': request.form.get('phone'),
            'role': request.form.get('role'),
            'created_at': utc_now()
        }
        mongo.db.contacts.insert_one(payload)
        return redirect(url_for('admin_dashboard'))
    contacts = list(mongo.db.contacts.find().sort('created_at', -1))
    return jsonify(contacts)


@app.route('/api/contacts/<contact_id>', methods=['DELETE'])
@admin_required
def delete_contact(contact_id):
    mongo.db.contacts.delete_one({'_id': contact_id})
    return jsonify({'status': 'deleted'})
