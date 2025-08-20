<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Laravel\Sanctum\HasApiTokens;

class Club extends Authenticatable
{
    use HasApiTokens, HasFactory;
    

    protected $table = 'clubs';

    protected $guarded = []; 

    protected $hidden = [
        'password',
    ];
}
