import 'dart:io';

import 'package:firebase_storage/firebase_storage.dart';
import 'package:uuid/uuid.dart';

import 'package:flutter_image_compress/flutter_image_compress.dart';
import 'package:path_provider/path_provider.dart' as path_provider;

class FirebaseImageService {
  static Future<String> uploadImgFireStorageFile({required File imageFile}) async {
    var uuid = new Uuid();

    Reference firebaseStorageRef = FirebaseStorage.instance.ref().child('profileImages').child("${uuid.v1()}.jpg");

    var uploadImg = await FirebaseImageCompressService.getCompressImageFile(imageFile);

    UploadTask uploadTask = firebaseStorageRef.putFile(uploadImg);

    var downloadUrl = await uploadTask;

    return (await downloadUrl.ref.getDownloadURL());
  }
}

class FirebaseImageCompressService {
  static Future<File> getCompressImageFile(File file) async {
    var uuid = new Uuid();
    var dir = await path_provider.getTemporaryDirectory();
    var targetPath = dir.absolute.path + uuid.v1() + '.jpg';

    var result = await FlutterImageCompress.compressAndGetFile(file.absolute.path, targetPath, quality: 70, minWidth: 600, minHeight: 600, rotate: 0);

    if (result != null) return File(result.path);
    return file;
  }
}
