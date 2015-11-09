from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from doctores.models import Item, List
from doctores.views import home_page


class TestPaginaPrincipal(TestCase):

    def test_direccion_root_resuleve_a_pagina_principal(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_retorna_el_html_correcto(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


class TestNuevaLista(TestCase):

    def test_guardar_una_peticion_POST(self):
        self.client.post(
            '/doctores/new',
            data={'item_text': 'Odontologia'}
        )
        self.assertEqual(Item.objects.count(), 1)
        nueva_area = Item.objects.first()
        self.assertEqual(nueva_area.text, 'Odontologia')

    def test_redirigir_despues_POST(self):
        response = self.client.post(
            '/doctores/new',
            data={'item_text': 'Odontologia'}
        )
        nueva_area = List.objects.first()
        self.assertRedirects(response, '/doctores/%d/' % (nueva_area.id,))


class TestNuevoDoctor(TestCase):

    def test_guardar_una_solicitud_POST_en_una_lista_existente(self):
        correct_list = List.objects.create()

        self.client.post(
            '/doctores/%d/add_item' % (correct_list.id,),
            data={'item_text': 'Nuevo doctor agregado a una lista'}
        )

        self.assertEqual(Item.objects.count(), 1)
        nuevo_doctor = Item.objects.first()
        self.assertEqual(nuevo_doctor.text, 'Nuevo doctor agregado a una lista')
        self.assertEqual(nuevo_doctor.list, correct_list)

    def test_redirige_a_la_vista_de_la_lista(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/doctores/%d/add_item' % (correct_list.id,),
            data={'item_text': 'Nuevo doctor agregado a una area ya creada'}
        )

        self.assertRedirects(response, '/doctores/%d/' % (correct_list.id,))


class ListViewTest(TestCase):

    def test_usa_la_lista_un_template(self):
        list_ = List.objects.create()
        response = self.client.get('/doctores/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_se_pasa_la_lista_correcta_al_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/doctores/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

    def test_la_lista_muestra_los_elementos_correctos(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Juan', list=correct_list)
        Item.objects.create(text='Pedro', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='Otro juan', list=other_list)
        Item.objects.create(text='Otro Pedro', list=other_list)

        response = self.client.get('/doctores/%d/' % (correct_list.id,))

        self.assertContains(response, 'Juan')
        self.assertContains(response, 'Pedro')
        self.assertNotContains(response, 'Otro juan')
        self.assertNotContains(response, 'Otro Pedro')


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        primer_doctor = Item()
        primer_doctor.text = 'Jun'
        primer_doctor.list = list_
        primer_doctor.save()

        segundo_doctor = Item()
        segundo_doctor.text = 'Zeratu'
        segundo_doctor.list = list_
        segundo_doctor.save()

        lista_guardada = List.objects.first()
        self.assertEqual(lista_guardada, list_)

        doctores_guardados = Item.objects.all()
        self.assertEqual(doctores_guardados.count(), 2)

        primer_doctor = doctores_guardados[0]
        segundo_doctor = doctores_guardados[1]
        self.assertEqual(primer_doctor.text, 'Jun')
        self.assertEqual(primer_doctor.list, list_)
        self.assertEqual(segundo_doctor.text, 'Zeratu')
        self.assertEqual(segundo_doctor.list, list_)
