<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Sanctum\HasApiTokens; // <-- add this
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Coach extends Model
{
    use HasApiTokens, HasFactory; // <-- include HasApiTokens here

    protected $table = 'coaches';
    protected $guarded = [];

    // Optional: hide password when returning model as JSON
    protected $hidden = [
        'password',
        'remember_token',
    ];
}
