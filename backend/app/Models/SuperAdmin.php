<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;

class SuperAdmin extends Authenticatable
{
    use HasApiTokens, Notifiable;

    protected $table = 'super_admin';

    // Allow all columns to be mass-assigned
    protected $guarded = [];

    protected $hidden = [
        'password', 'remember_token',
    ];
}
