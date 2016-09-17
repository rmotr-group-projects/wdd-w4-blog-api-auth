# Blog API auth

Today we will expand the Blog API we built in the previous groups work.

The data model will look like similar, but we will replace the `Author` model with a custom Django `User` model. That will allow us to write more complex authentication and permissions rules. Now the blog `Entry` model will have a `ForeignKey` pointing to `User` instead of `Author`.

## AK and SK Authentication

We will need to change the authentication of the API completely. In the previous project, we were not using authentication at all. Now we will create two new custom authentication classes: `UserAccesskeyAuthentication` and `UserSecretkeyAuthentication`.

We must require AK + SK for any non-safe action (meaning, actions that will write data into the app), and only AK for any other read-only action.

The API user must send the AK as a GET parameter (ie: `?accesskey=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`). SK, on the other hand, will be sent using a custom HTTP header:
```
X-Secret-Key: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
```
You will notice that in the tests we are using `HTTP_X_SECRET_KEY` header name instead. That's because the way how the Django test runner handles HTTP headers, but if you are using the API out of the Django tests, you will need to use `X-Secret-Key` instead.

This logic must be implemented using a custom Authentication subclass for AK and other one for SK Auth. You will need to manage to configure the settings properly to run the sequentially in the proper way.


### `GET /blogs` with AK
![get](http://i.imgur.com/nDftmwO.png)


### `POST /blogs` with AK and SK
![post](http://i.imgur.com/kZLeBp3.png)

## Permission

Once you have the authentication working properly, you will need to configure a custom Permission class.

We need to restrict write actions for the `Entry` model, so only the users who created the entry can modify them. That means, if a user out of the original authors of the Entry try to update or delete the entry, we need to return a `HTTP_403_FORBIDDEN` response.

For that we need to write a custom Permission class and configure it for the `Entry` view set.

### `PATCH /entries/:id` without permission
![patch](http://i.imgur.com/d9tonY1.png)

## Note
As we are replacing the `Author` model with `User`, we will need to take same extra considerations while writting the endpoints.

For example, when you POST to create a new `User`, make sure the password is saved hashed instead of as plain text.

Same while updating. If the password changed, make sure to hash the password before saving it.

These helper functions could be useful for this particular requirement:
[https://docs.djangoproject.com/es/1.10/topics/auth/passwords/#module-django.contrib.auth.hashers](https://docs.djangoproject.com/es/1.10/topics/auth/passwords/#module-django.contrib.auth.hashers)
