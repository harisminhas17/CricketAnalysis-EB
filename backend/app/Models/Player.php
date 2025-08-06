<?php

namespace App\Models;
use Illuminate\Notifications\Notifiable;
use Illuminate\Database\Eloquent\Model;

class Player extends Model
{
    use HasApiTokens, Notifiable;
    protected $table = 'players';
    protected $guarded = [];
}
