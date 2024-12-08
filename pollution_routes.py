from flask import Blueprint, render_template, request, flash, redirect, url_for
import pandas as pd


pollution_bp = Blueprint('pollution', __name__, url_prefix='/pollution')


@pollution_bp.route('/view-pollution-data')
def view_pollution_data():
   try:
       data = pd.read_csv('data/bay_area_pollution_data.csv')


       selected_location = request.args.get('location', '')
       if selected_location:
           data = data[data['Location'] == selected_location]


       table_html = data.to_html(classes='table table-striped', index=False)
       locations = data['Location'].unique().tolist()


   except Exception as e:
       flash(f"Error reading CSV file: {str(e)}", "danger")
       return redirect(url_for('home'))


   return render_template(
       'pollution-data-view-template.html',
       table=table_html,
       locations=locations,
       selected_location=selected_location
   )
