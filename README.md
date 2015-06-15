Daily
=========================


TODO list
-------------------

translate tag
comitar bootstrap bottle
rename brand
fix social html
fix js css
test script
load videos and tags etc
deploy heroku
think of name



layout:
Bootstrap heroku
deploy
Add redis cache
async view
celery/redis
schedule config
user
favorites
recommend link
report video
comments
tags
i18n en pt
share


Add links
-------------------

http -f POST http://localhost:8000/api/v1/link "Authorization:Token nice" url="" tags="tag1,tag2,tag3" text=""


http -f POST http://localhost:8000/api/v1/link "Authorization:Token nice" url="" tags="tag3,tag4,tag5" text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis quam ex, faucibus vitae ex a, aliquam gravida odio. Ut tempus erat at urna porttitor, eu gravida arcu commodo. Duis nisl ex, suscipit eget leo a, vulputate aliquam tellus. Mauris vitae vestibulum nisl, eu mollis purus. Duis magna mi, faucibus in tortor lacinia, pharetra luctus risus. Nulla pretium purus non risus mollis, ut interdum velit placerat. Maecenas pellentesque at mi sed laoreet.

Vestibulum congue tempor ante, nec dapibus leo consequat quis. Proin mollis libero tincidunt lorem sodales molestie. Vestibulum egestas elit id ex cursus pretium. In ultricies ut ligula eget congue. Integer finibus nisi scelerisque tortor lacinia, quis bibendum sapien ornare. Morbi purus libero, ornare eget tellus sit amet, cursus sollicitudin neque. Aenean dapibus ut ligula eget consectetur. Donec tempus euismod urna at tincidunt. Praesent et mi sit amet sapien lacinia laoreet. Suspendisse potenti. Proin id gravida mauris. Duis quis fermentum lacus. Nulla mollis lorem neque, non ultricies erat tincidunt sed. Nulla viverra gravida rutrum.

Praesent pharetra nisl eget ipsum rutrum, vel lobortis mauris elementum. Phasellus eget dui congue, pharetra nisl a, aliquam enim. Donec enim nunc, dignissim id sem sit amet, placerat cursus nulla. Duis pulvinar sed lorem et egestas. Cras vehicula augue ac elit porttitor mattis. Morbi scelerisque nisl quis dolor consectetur, vitae venenatis lectus convallis. Donec sed auctor enim. Praesent eu elementum magna, id aliquam neque. Morbi in euismod enim. Vestibulum fringilla laoreet dignissim. Curabitur lobortis nulla massa, ac varius lorem egestas vulputate. Donec condimentum leo et est ultricies lobortis. Mauris id tortor congue, laoreet augue quis, rhoncus eros. Sed cursus porta suscipit. Donec vel neque at lectus cursus dignissim.

Phasellus cursus, est nec porttitor placerat, quam urna dignissim ex, mattis hendrerit nisl magna et felis. Vivamus cursus sapien sed velit commodo molestie. Sed semper condimentum lorem eleifend posuere. Cras ac erat sit amet ipsum malesuada elementum. Ut fringilla interdum magna, eget pretium nibh consequat a. Etiam id dui id justo placerat gravida. In tincidunt dui sapien, id congue nisl malesuada vel. Sed tincidunt justo eget tellus euismod fermentum. Quisque ac interdum nisl. Nulla mattis egestas pretium. Vestibulum blandit risus non velit cursus, eu euismod neque fringilla. Donec in metus et massa vestibulum aliquam. Suspendisse in maximus nibh, vitae egestas lorem.

Donec interdum augue lacus, convallis egestas libero imperdiet sed. Praesent pharetra semper risus, quis dignissim ex laoreet nec. Sed pretium sapien id tortor semper, vitae fringilla ante ullamcorper. Morbi vel nisl vel dolor auctor aliquet eget id odio. In libero enim, ultricies et tellus sit amet, pharetra ultrices metus. Curabitur mattis id sem sed consequat. Curabitur mollis augue elit, et pellentesque dui bibendum non. Praesent ullamcorper eget orci ac sollicitudin. Maecenas quis commodo ex. Pellentesque feugiat quis massa sit amet bibendum. Proin lorem tellus, accumsan quis consequat et, lobortis vitae lectus. Aliquam erat volutpat. Ut non ullamcorper mi, sit amet euismod sem. Mauris mollis ex sed mollis molestie."


Publish links
-------------------

import connect_mongo
from app.models import *
Link.objects(revised=None).update(revised=True)

http -f -h POST http://localhost:8000/api/v1/link/publish "Authorization:Token nice"


Report
-------------------

http GET http://localhost:8000/api/v1/report "Authorization:Token nice"