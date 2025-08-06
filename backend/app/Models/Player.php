<?php

namespace App\Models;
use Illuminate\Notifications\Notifiable;
use Illuminate\Database\Eloquent\Model;
use Laravel\Sanctum\HasApiTokens;

class Player extends Model
{
    use HasApiTokens, Notifiable;
    protected $table = 'players';
    protected $guarded = [];
}
