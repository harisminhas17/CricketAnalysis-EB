<?php

namespace App\HelperFunctions;

class HelperFunctions
{
    public static function uploadImage($image, $folder)
    {
        $imageName = time() . '_' . uniqid() . '.' . $image->getClientOriginalExtension();
        $path = public_path('uploads/' . $folder);

        if (!file_exists($path)) {
            mkdir($path, 0777, true);
        }

        $image->move($path, $imageName);

        return 'uploads/' . $folder . '/' . $imageName;
    }
}
