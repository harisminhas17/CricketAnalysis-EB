<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class SuperAdmin extends Model
{
    use HasFactory;

    protected $fillable = [
        'name',
        'email',
        'password',
        'phone_number',
        'profile_image',
        'state',
        'city',
        'address',
        'zip_code',
        'country',
        'is_active'
    ];
   

    // Hide sensitive attributes
    protected $hidden = [
        'password',
    ];
}
