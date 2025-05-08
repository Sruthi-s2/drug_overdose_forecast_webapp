from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from services.admin_service import call_insert_record, fetch_states_for_admin
from services.overdose_service import get_filter_options
from repository.overdose_repo import update_overdose_record, find_single_record, find_conflicting_record
from repository.overdose_repo import find_records_for_deletion
from werkzeug.security import generate_password_hash
from repository.user_repo import create_user, get_filtered_users, delete_user_by_emails
from repository.overdose_repo import delete_overdose_records, delete_by_ids
from werkzeug.security import generate_password_hash

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/admin')
def admin_panel():
    if session.get('role') != 'admin':
        return redirect(url_for('auth_routes.login_page'))
    return render_template('admin_select_action.html')


@admin_routes.route('/admin/<action>')
def admin_action_page(action):
    if session.get('role') != 'admin':
        return redirect(url_for('auth_routes.login_page'))

    if action == "insert":
        states = fetch_states_for_admin()
        indicators = get_filter_options().get('indicators', [])
        return render_template(
            'admin_insert.html',
            states=[s['name'] for s in states],
            state_map={s['name']: s['code'] for s in states},
            indicators=indicators
        )

    elif action == "delete":
        filters = get_filter_options()
        return render_template(
            'admin_delete.html',
            states=filters['states'],
            years=filters['years'],
            months=filters['months'],
            indicators=filters['indicators']
        )


    elif action == "modify":
        filters = get_filter_options()
        return render_template(
            'admin_modify.html',
            states=filters['states'],
            years=filters['years'],
            months=filters['months'],
            indicators=filters['indicators']
        )


    elif action == "manage_users":
        return render_template('admin_user.html')

    return redirect(url_for('admin_routes.admin_panel'))


@admin_routes.route('/admin/insert_record', methods=['POST'])
def handle_insert_record():
    data = {
        "year": request.form['year'],
        "month": request.form['month'],
        "state_name": request.form['state_name'],
        "state_code": request.form['state_code'],
        "indicator": request.form['indicator'],
        "no_of_deaths": request.form['no_of_deaths']
    }

    try:
        call_insert_record(data)
        flash("Record inserted successfully!", "success")
    except Exception as e:
        flash(f"Failed to insert record: {str(e)}", "danger")

    return redirect(url_for('admin_routes.admin_action_page', action='insert'))



@admin_routes.route('/admin/fetch_record', methods=['POST'])
def fetch_record_for_modification():

    filters = {
        "state": request.form['state'],
        "year": int(request.form['year']),
        "month": request.form['month'],
        "indicator": request.form['indicator']
    }

    record = find_single_record(filters)
    if record:
        
        filters = get_filter_options()
        return render_template(
            'admin_modify.html',
            record=record,
            states=filters['states'],
            years=filters['years'],
            months=filters['months'],
            indicators=filters['indicators'],
            selected=filters
        )
    else:
        flash("No matching record found.", "warning")
        return redirect(url_for('admin_routes.admin_action_page', action='modify'))
    
    

@admin_routes.route('/admin/update_record', methods=['POST'])
def update_record():
    record_id = request.form['_id']
    updated_data = {
        "year": int(request.form['year']),
        "month": request.form['month'],
        "state": {
            "name": request.form['state_name'],
            "code": request.form['state_code']
        },
        "indicator": request.form['indicator'],
        "no_of_deaths": float(request.form['no_of_deaths'])
    }

   
    conflict = find_conflicting_record(updated_data, record_id)
    if conflict:
        flash("Update failed: another record with the same values already exists.", "danger")
        return redirect(url_for('admin_routes.admin_action_page', action='modify'))

    try:
        update_overdose_record(record_id, updated_data)
        flash("Record updated successfully.", "success")
    except Exception as e:
        flash(f"Update failed: {str(e)}", "danger")

    return redirect(url_for('admin_routes.admin_action_page', action='modify'))


@admin_routes.route('/admin/delete_records', methods=['POST'])
def delete_records():

    delete_mode = request.form.get("delete_mode")

    if delete_mode == "selected":
        selected_ids = request.form.getlist("selected_ids")
        if not selected_ids:
            flash("No records selected for deletion.", "warning")
        else:
            deleted = delete_by_ids(selected_ids)
            flash(f"{deleted.deleted_count} selected record(s) deleted.", "success")

    elif delete_mode == "all":
        filter_criteria = {
            "year": int(request.form['year']),
            "state.name": request.form['state'],
            "indicator": request.form['indicator']
        }
        selected_months = request.form.getlist("months")
        if selected_months:
            filter_criteria["month"] = {"$in": selected_months}

        result = delete_overdose_records(filter_criteria)
        flash(f"{result.deleted_count} matching record(s) deleted.", "success")

    return redirect(url_for('admin_routes.admin_action_page', action='delete'))




@admin_routes.route('/admin/preview_deletion', methods=['POST'])
def preview_deletion():
    filters = get_filter_options()
    selected = {
        "state": request.form['state'],
        "year": request.form['year'],
        "indicator": request.form['indicator'],
        "months": request.form.getlist("months")
    }

    # build criteria
    query = {
        "state.name": selected["state"],
        "year": int(selected["year"]),
        "indicator": selected["indicator"]
    }
    if selected["months"]:
        query["month"] = {"$in": selected["months"]}

    # fetch matching records
    records = find_records_for_deletion(query)

    return render_template(
        'admin_delete.html',
        states=filters['states'],
        years=filters['years'],
        months=filters['months'],
        indicators=filters['indicators'],
        selected=selected,
        records=records
    )


@admin_routes.route('/admin/user_management')
def user_management():
    if session.get('role') != 'admin':
        return redirect(url_for('auth_routes.login_page'))

    email = request.args.get('email', '').strip()
    role = request.args.get('role', '').strip()
    users = get_filtered_users(email=email, role=role)
    return render_template('admin_user.html', users=users)


@admin_routes.route('/admin/delete_selected_users', methods=['POST'])
def delete_selected_users():
    emails = request.form.getlist('emails')
    if not emails:
        flash("No users selected for deletion.", "warning")
    else:
        delete_user_by_emails(emails)
        flash(f"{len(emails)} user(s) deleted successfully.", "success")
    return redirect(url_for('admin_routes.user_management'))


@admin_routes.route('/admin/create_user_record', methods=['POST'])
def create_user_record():
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    hashed = generate_password_hash(password)
    try:
        create_user(email, hashed, role)
        flash("User created successfully!", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('admin_routes.user_management'))
