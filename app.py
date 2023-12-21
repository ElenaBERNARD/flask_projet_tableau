#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, flash, url_for, abort  # application WSGI

app = Flask(__name__)
app.secret_key = 'clesecretegenrevraimentimpossbleatrouveruwu'

from flask import session, g
import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="localhost",                 # à modifier
            user="drg0n",                     # à modifier
            password="2302",                # à modifier
            database="BDD_drg0n",        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
@app.route('/home')
def showIndex():
    print('Affichage de l\'index')
    return render_template('index.html')

##################################################
##########             SHOW             ##########
##################################################

@app.route('/tableau/show')
def show_tableau():
    mycursor = get_db().cursor()
    sql=''' SELECT tableau.*, type_epoque.libelle AS type_epoque_libelle
    FROM tableau
    LEFT JOIN type_epoque ON tableau.type_epoque_id = type_epoque.id_type_epoque;
    '''
    mycursor.execute(sql)
    liste_tableaux = mycursor.fetchall()
    return render_template('tableau/show_tableau.html', Tableaux=liste_tableaux)

@app.route('/type_epoque/show')
def show_type_epoque():
    mycursor = get_db().cursor()
    sql='''SELECT *
    FROM type_epoque;'''
    mycursor.execute(sql)
    liste_type_epoques = mycursor.fetchall()
    return render_template('type_epoque/show_type_epoque.html', Type_epoques=liste_type_epoques)


##################################################
##########             ADD              ##########
##################################################


@app.route('/tableau/add', methods=['GET'])
def add_tableau():
    mycursor = get_db().cursor()
    sql=''' SELECT *
    FROM type_epoque'''
    mycursor.execute(sql)
    liste_type_epoques = mycursor.fetchall()
    return render_template('tableau/add_tableau.html', Type_epoques=liste_type_epoques)

@app.route('/tableau/add', methods=['POST'])
def valid_add_tableau():
    nom_tableau = request.form.get('nom_tableau')
    prix_assurance = request.form.get('prix_assurance')
    date_realisation = request.form.get('date_realisation', '')
    peintre = request.form.get('peintre', '')
    localisation_musee = request.form.get('localisation_musee', '')
    photo = request.form.get('photo', '')
    mouvement = request.form.get('mouvement', '')
    type_epoque_id = request.form.get('type_epoque_id', '')
    message = 'Ajout du tableau : Epoque :' + type_epoque_id + ' - nom :' + nom_tableau + ' - prix assurance :' + prix_assurance + ' - date realisation :' + date_realisation + ' - peintre :' + peintre + ' - localisation musee :' + localisation_musee + ' - photo :' + photo + ' - mouvment :' + mouvement
    print(message)
    mycursor = get_db().cursor()
    tuple_param=(nom_tableau, prix_assurance, date_realisation, peintre, localisation_musee, photo, mouvement, type_epoque_id)
    sql="INSERT INTO tableau(nom_tableau, prix_assurance, date_realisation, peintre, localisation_musee, photo, mouvement, type_epoque_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    flash(message, 'alert-success')
    return redirect('/tableau/show')


@app.route('/type_epoque/add', methods=['GET'])
def add_type_epoque():
    return render_template('type_epoque/add_type_epoque.html')
    
@app.route('/type_epoque/add', methods=['POST'])
def valid_add_type_epoque():
    libelle = request.form.get('libelle')
    annee_debut = request.form.get('annee_debut')
    annee_fin = request.form.get('annee_fin', '')
    message = 'Ajout d un type d epoque : libelle:' + libelle + ' annee debut :' + annee_debut + ' - annee fin :' + annee_fin
    mycursor = get_db().cursor()
    tuple_param=(libelle, annee_debut, annee_fin)
    sql="INSERT INTO type_epoque(libelle, annee_debut, annee_fin) VALUES (%s, %s, %s);"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    flash(message, 'alert-success')
    return redirect('/type_epoque/show')


##################################################
##########             EDIT             ##########
##################################################


@app.route('/tableau/edit', methods=['GET'])
def edit_tableau():
    id_tableau = int(request.args.get('id_tableau', ''))
    mycursor = get_db().cursor()
    sql=''' SELECT *
    FROM tableau
    WHERE id_tableau=%s;'''
    sql2='''SELECT *
    FROM type_epoque;'''
    tuple_param=(id_tableau)
    mycursor.execute(sql,tuple_param)
    tableau = mycursor.fetchone()
    mycursor.execute(sql2)
    type_epoques = mycursor.fetchall()
    return render_template('tableau/edit_tableau.html', Tableau=tableau, Type_epoques=type_epoques)

@app.route('/tableau/edit', methods=['POST'])
def valid_edit_tableau():
    id_tableau = request.form.get('id_tableau')
    nom_tableau = request.form.get('nom_tableau')
    prix_assurance = request.form.get('prix_assurance')
    date_realisation = request.form.get('date_realisation', '')
    peintre = request.form.get('peintre', '')
    localisation_musee = request.form.get('localisation_musee', '')
    photo = request.form.get('photo', '')
    mouvement = request.form.get('mouvement', '')
    type_epoque_id = request.form.get('type_epoque_id', '')
    message = u'tableau modifié id :'+ id_tableau + \
              ' nomTableau: '+ nom_tableau + \
              '- prixAssurance :' + prix_assurance + \
              ' - dateRealisation:' + date_realisation + \
              ' - peintre:'+  peintre + \
              ' - localisationMusee:' + localisation_musee + \
              ' - photo:' + photo + \
              ' - mouvement:' + mouvement + \
              ' - typeEpoque_id:' + type_epoque_id
    mycursor = get_db().cursor()
    tuple_param=(nom_tableau, prix_assurance, date_realisation, peintre, localisation_musee, photo, mouvement, type_epoque_id, id_tableau)
    sql="UPDATE tableau SET nom_tableau=%s, prix_assurance=%s, date_realisation=%s, peintre=%s, localisation_musee=%s, photo=%s, mouvement=%s, type_epoque_id=%s WHERE id_tableau=%s;"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    flash(message, 'alert-success')
    return redirect('/tableau/show')


@app.route('/type_epoque/edit', methods=['GET'])
def edit_type_epoque():
    id_type_epoque = int(request.args.get('id_type_epoque', ''))
    mycursor = get_db().cursor()
    sql=''' SELECT *
    FROM type_epoque
    WHERE id_type_epoque=%s;'''
    tuple_param=(id_type_epoque)
    mycursor.execute(sql,tuple_param)
    type_epoque = mycursor.fetchone()
    return render_template('type_epoque/edit_type_epoque.html', Type_epoque=type_epoque)

@app.route('/type_epoque/edit', methods=['POST'])
def valid_edit_type_epoque():
    id_type_epoque = request.form.get('id_type_epoque')
    libelle = request.form.get('libelle')
    annee_debut = request.form.get('annee_debut')
    annee_fin = request.form.get('annee_fin', '')
    message=u'type epoque modifié, id: ' + id_type_epoque + " libelle : " + libelle + " - annee debut :" + annee_debut + " - annee fin :" + annee_fin
    mycursor = get_db().cursor()
    tuple_param=(libelle, annee_debut, annee_fin, id_type_epoque)
    sql="UPDATE type_epoque SET libelle=%s, annee_debut=%s, annee_fin=%s WHERE id_type_epoque=%s;"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    flash(message, 'alert-success')
    return redirect('/type_epoque/show')


##################################################
##########            DELETE            ##########
##################################################


@app.route('/tableau/delete', methods=['GET'])
def delete_tableau():
    id_tableau = request.args.get('id_tableau', '')
    return render_template('tableau/delete_tableau.html', id_tableau=id_tableau)

@app.route('/tableau/delete', methods=['POST'])
def valid_delete_tableau():
    id_tableau = request.form.get('id_tableau',0)
    message=u'Un tableau a été supprimé, id : ' + id_tableau
    mycursor = get_db().cursor()
    tuple_param = (id_tableau)
    sql="DELETE FROM tableau WHERE id_tableau=%s;"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    flash(message, 'alert-warning')
    return redirect('/tableau/show')


@app.route('/type_epoque/delete', methods=['GET'])
def delete_type_epqoue():
    mycursor = get_db().cursor()
    id_type_epoque = request.args.get('id_type_epoque', '')
    tuple_delete = (id_type_epoque)
    
    sql = ''' SELECT *
        FROM type_epoque
        WHERE id_type_epoque=%s'''
    mycursor.execute(sql, tuple_delete)
    type_epoque_current = mycursor.fetchone()
    
    sql2=''' SELECT tableau.*, type_epoque.libelle AS type_epoque_libelle
    FROM tableau
    LEFT JOIN type_epoque ON tableau.type_epoque_id = type_epoque.id_type_epoque
    WHERE type_epoque_id=%s;
    '''
    mycursor.execute(sql2, tuple_delete)
    liste_tableaux = mycursor.fetchall()
    return render_template('type_epoque/delete_type_epoque.html', type_epoque_current=type_epoque_current, Tableaux=liste_tableaux)

@app.route('/type_epoque/delete_control', methods=['POST'])
def delete_control_type_epoque():
    mycursor = get_db().cursor()
    
    #Supression du tableau
    id_tableau = request.form.get('id_tableau',0)
    message=u'Un tableau a été supprimé, id : ' + id_tableau
    
    tuple_param = (id_tableau)
    sql="DELETE FROM tableau WHERE id_tableau=%s;"
    mycursor.execute(sql,tuple_param)
    get_db().commit()

    #Renvoie vers la page
    id_type_epoque = request.form.get('id_type_epoque', '')
    tuple_delete = (id_type_epoque)
    
    sql = ''' SELECT *
        FROM type_epoque
        WHERE id_type_epoque=%s'''
    mycursor.execute(sql, tuple_delete)
    type_epoque_current = mycursor.fetchone()
    
    sql2 = ''' SELECT *
        FROM tableau
        WHERE type_epoque_id=%s;'''
    mycursor.execute(sql2, tuple_delete)
    liste_tableau = mycursor.fetchall()
    sql3 = ''' SELECT *
        FROM type_epoque'''
    mycursor.execute(sql3)
    liste_type_epoque = mycursor.fetchall()
    
    flash(message, 'alert-warning')
    return render_template('type_epoque/delete_type_epoque.html', type_epoque_current=type_epoque_current, Tableaux=liste_tableau, Type_epoques=liste_type_epoque)


@app.route('/type_epoque/delete', methods=['POST'])
def valid_delete_type_epoque():
    id_type_epoque = request.form.get('id_type_epoque',0)
    message=u'Un type depoque a été supprimé, id : ' + id_type_epoque
    mycursor = get_db().cursor()
    tuple_param = (id_type_epoque)
    sql="DELETE FROM type_epoque WHERE id_type_epoque=%s;"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    flash(message, 'alert-warning')
    return redirect('/type_epoque/show')


##################################################
##########             ETAT             ##########
##################################################


@app.route('/tableau/etat')
def etat_tableau():
    mycursor = get_db().cursor()
    sql=''' SELECT 
    SUM(prix_assurance) AS total_prix_assurance,
    COUNT(*) AS nb_tableaux
    FROM tableau;
    '''
    mycursor.execute(sql)
    prix_assurance = mycursor.fetchone()
    sql2='''SELECT type_epoque.id_type_epoque, type_epoque.libelle,
    COUNT(tableau.id_tableau) AS nb_tableau_par_type,
    SUM(tableau.prix_assurance) AS total_prix_par_type
    FROM tableau
    JOIN type_epoque ON tableau.type_epoque_id = type_epoque.id_type_epoque
    GROUP BY tableau.type_epoque_id;'''
    mycursor.execute(sql2)
    liste_tableaux = mycursor.fetchall()
    return render_template('tableau/etat_tableau.html', Prix_assurance=prix_assurance, Tableaux=liste_tableaux)


##################################################
##########            FILTRE            ##########
##################################################


@app.route('/tableau/filtre', methods=['GET'])
def filtre_tableau():
    filter_nom = request.args.get('filter_nom', None)
    filter_min = request.args.get('filter_min', None)
    filter_max = request.args.get('filter_max', None)
    filter_items = request.args.getlist('filter_items', None)
    if filter_nom and filter_nom != "":
        message = u'filtre sur le nom : ' + filter_nom
        flash(message, 'alert-success')
    min = str(filter_min).replace(' ', '').replace(',', '.')
    max = str(filter_max).replace(' ', '').replace(',', '.')
    if min.replace('.', '', 1).isdigit() and max.replace('.', '', 1).isdigit():
        if float(min) < float(max):
            message = u'fitre avec un numerique entre : ' + min + ' et ' + max
            flash(message, 'alert-success')
        else:
            message = u'min doit être plus petit que max'
            flash(message, 'alert-warning')
    elif min != '' or max != '':
        message = u'min et max doivent etre des numeriques positifs'
        flash(message, 'alert-warning')

    if filter_items and filter_items != []:
        message = u'Case a cocher selectionnée : '
        for case in filter_items:
            message += ' id: '+case + ' ; '
        flash(message, 'alert-success')
    return render_template('tableau/filtre_tableau.html', tableaux=tableaux, typesEpoque=typesEpoque)


###     FIN DU CODE     ###


@app.route('/')
def show_accueil():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)