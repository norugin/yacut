from flask import render_template, redirect, flash
from .forms import URLForm
from .models import URLMap
from . import app, db


@app.route('/', methods=('GET', 'POST',))
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        url_map = URLMap()
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = url_map.get_unique_short_id()

        if URLMap.query.filter_by(short=custom_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.',
                  'error')
            return render_template('index.html', form=form)

        if not url_map.is_valid_short_id(custom_id):
            flash('В ссылке присутствуют невалидные символы', 'error')
            return render_template('index.html', form=form)

        url_map = URLMap(original=form.original_link.data, short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        return render_template('index.html', form=form, url_map=url_map)

    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def short_link_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)