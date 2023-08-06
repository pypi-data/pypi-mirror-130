(mama profile) ไลบรารี่สำหรับใช้เรียน Python OOP by mama profile
================================================================

PyPi: https://pypi.org/project/mamaprofile/

Python OOP+ วิธีสร้าง Library เป็นของตัวเอง+ อัพโหลด Package ไปยัง
PyPI.org

โปรแกรมนี้ใช้สำหรับสอนการเขียนโปรแกรมแบบ OOP

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

   pip install mamaprofile

วิธีใช้งานแพ็คเพจนี้
~~~~~~~~~~~~~~~~~~~~

-  เปิด IDLE ขึ้นมาแล้วพิมพ์…

\```python from mamaprofile import profile

::

   print('start')
   me = profile('Mama')             
   print(me)
   print(me.name)                  
   me.company = 'ABC'
   me.show_email()                  
   print('----------------')

   me.hobby = ['Youtuber','Reading','Sleeping']
   me.show_hobby()

   other = profile('Papa')
   print(other)
   print(other.name)
   other.show_email()

   art = other.show_ascii_art()
   print(art)
   print('\n',other.show_ascii_art())     

พัฒนาโดย: mamaprofile
