from flask import Blueprint, render_template, request, flash, redirect, url_for
import pandas as pd


traffic_bp = Blueprint('traffic', __name__)


@traffic_bp.route('/view-traffic-data')
def view_traffic_data():
  try:
      data = pd.read_csv('data/bay_area_traffic_data.csv')


      selected_collision_type = request.args.get('collision_type', '')
      if selected_collision_type:
          data = data[data['TypeOfCollision'] == selected_collision_type]


      table_html = data.to_html(classes='table table-striped', index=False)


      collision_types = data['TypeOfCollision'].unique().tolist()


  except Exception as e:
      flash(f"Error reading CSV file: {str(e)}", "danger")
      return redirect(url_for('home'))


  return render_template(
      'traffic-data-view-template.html',
      table=table_html,
      collision_types=collision_types,
      selected_collision_type=selected_collision_type
  )