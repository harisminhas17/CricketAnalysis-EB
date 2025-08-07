<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;

class SuperAdmin extends Authenticatable
{
    use HasApiTokens, Notifiable;

    protected $table = 'super_admins';

    protected $fillable = [
        'name', 'email', 'password', 'phone_number', 'profile_image',
        'state', 'city', 'address', 'zip_code', 'country', 'is_active',
    ];

    protected $hidden = [
        'password', 'remember_token',
    ];
}
