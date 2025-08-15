<?php

namespace Database\Seeders;

use App\Models\PlayerRole;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Carbon\Carbon;

class PlayerRoleSeeder extends Seeder
{
    public function run()
    {

        $now = Carbon::now();

        $roles = [
            ['id' => 1, 'name' => 'Batsman'],
            ['id' => 2, 'name' => 'Bowler'],
            ['id' => 3, 'name' => 'All-Rounder'],
            ['id' => 4, 'name' => 'Wicket Keeper'],
            ['id' => 5, 'name' => 'Captain'],
            ['id' => 7,  'name' => 'Fast Bowler'],
        ];

        foreach ($roles as &$role) {
            $role['sport_type'] = 'cricket';
            $role['created_at'] = $now;
            $role['updated_at'] = $now;
        }

        PlayerRole::insert($roles);
    }
}
