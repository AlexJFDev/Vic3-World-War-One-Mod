s1 = '''Acton Albricci Agnes Airenti Amaretti Ara Arminjon Arnulfo Arrifo Asproni Astengo Avigdor Avondo
		Badoglio Baldissera Baratieri Bava-Beccaris Baldassi Benci Baino Barbier BeldI_ Bellono Benintendi Berruti Bersezio Berti Bertini Bertoldi Bezzi Biancheri Bianchetti Bianchi Billiet Blanc Bo Bolmida Bona Borella Botta Bottero Brignone Brofferio Brunati Brunet Brunier Bruschetti Buffa Buraggi Buttini
		Cadorna Cagni Canevaro Capello Caviglia Ceccherini Cialdini Cusani Cabella Caboni Cambieri Campana Canalis Cantara Capriolo Carquet Carta Casaretto Cassinis Castelli Cavalli Cavallini Chenal Chiaves ChiO_ Cobianchi Colli Cornero Correnti Corsi Costa Crosa Cugia
		Dezza Demaria Depretis Durando Daziani Decandia Delfino Delitala
		Emo
		Fanti Fara Filomarino Fara Farina Farini Ferraciu Fescot
		Garibaldi Giardino Govone Gallenga Gallisai Gallo Galvagno Gastinelli Genina Gerbore Germanetti Geymet Ghiglini Gianolio Gilardini Ginet Giovanola Graffigna Grixoni Guglianetti Guillet
		Imperiali Isola
		Lachenal Lanza Louaraz
		Malan La_Marmora Mambretti Menabrea Mozzoni Mameli Mamiani Mantelli Marassi Mari Marongiu Martelli Martin Mathieu Mautino Mazza Melegari Mellana Menabrea Mezzena Michelini Miglietti Miglioretti Minoglio Moia Mongellaz Monticelli Mossi Musso
		Naytana Niccolini Nino Notta
		Orengo Oytana
		Pelloux Perruchetti Pianelli Porro Presbitero Paleocapa Pallavicino Pallieri Pareto Pateri Pescatore Peyrone Pezzani Piacenzi Piane Picinelli Pistone Polleri Polto Porqueddu Pugioni
		Quaglia
		Ramorino Ricotti-Magnani Rattazzi Ravina Rezasco Riccardi Ricci Richetta Robecchi Roberti Rocci Rodini Rossi Rubin
		Sacchi Saletta Sanna Solari Sanguineti Sanna_Denti Sanna_Sanna Sappa Saracco Sauli Scano Scapini Sella Serra Sineo Siotto_Pintor Solari Spano Spinola Sulis
		Tecchio Tegas Tola Torelli Tuveri
		Vaccari Valerio Valvassori Vicari
		Zupelli Zirio'''
s2 = '''Anfora Avitabile Alianelli Antonelli Assanti Acclavio
		Barberini-Colonna Bonaccorsi Benci Bozzelli Baldacchini Briganti Bausan Bianchini
		Caraga Cattaneo Chigi Clary Cosenz Cianciulli Cuoco Costa Campagna Capocci Capasso Croce Carrascosa Colletta
		Diaz Durini Delfico
		Ferrari Filangieri Filioli Fergola Fardella Forteguerri Ferri Fortunato
		Gironda Gravina Grifeo Garzia Gagliardo Galdi Guarini Genoino Gussone Gio Giannuzzi Galletti
		Imbriani Intonti
		Lanza Lombardo Lunardi Landi Lanza Longobardi
		Molinelli Mezzacapo Milano Morelli
		Nunziante Naselli
		Orsini Ottaviani Oliva
		Pironti Pepe Poerio Palmieri Persico Parisi PaternO_ Pianell Pignatelli Pionati Parisio
		Quandel
		Ritucci Ruggiero Romano Rosaroll Ricciardi Rosica
		Scammacca Scovazzo Sansone Sannia Schipa Silvati Settimo Scialoja Statella Santangelo
		Torlonia Turrisi Troya Tommasi Tenore Tafuri Torelli Tardio Troisi
		Vernazza Valiante Vignale Vecchione
		Zunica Zurlo'''

def sort_key(text):
    return text.lower().replace('d_', '').replace('di_', '').replace('de_', '')

names1 = set(s1.replace('\n\t\t', ' ').split(' '))
names2 = set(s2.replace('\n\t\t', ' ').split(' '))

names = sorted(list(names1.union(names2)), key=sort_key)

try:
    names.remove('')
except ValueError:
    pass
first_letter = 'a'
for name in names:
    if first_letter != sort_key(name)[0]:
        first_letter = sort_key(name)[0]
        print()
    print(name, end=' ')
