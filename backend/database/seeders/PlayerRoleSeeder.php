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
            ['id' => 1,  'name' => 'Batsman'],
            ['id' => 2,  'name' => 'Bowler'],
            ['id' => 3,  'name' => 'All-Rounder'],
            ['id' => 4,  'name' => 'Wicket Keeper'],
            ['id' => 5,  'name' => 'Opening Batsman'],
            ['id' => 6,  'name' => 'Middle Order Batsman'],
            ['id' => 7,  'name' => 'Fast Bowler'],
            ['id' => 8,  'name' => 'Medium Pace Bowler'],
            ['id' => 9,  'name' => 'Off Spin Bowler'],
            ['id' => 10, 'name' => 'Leg Spin Bowler'],
            ['id' => 11, 'name' => 'Left Arm Fast Bowler'],
            ['id' => 12, 'name' => 'Right Arm Fast Bowler'],
            ['id' => 13, 'name' => 'Left Arm Spinner'],
            ['id' => 14, 'name' => 'Right Arm Spinner'],
            ['id' => 15, 'name' => 'Captain'],
            ['id' => 16, 'name' => 'Vice Captain'],
            ['id' => 17, 'name' => 'Wicket Keeper Batsman'],
            ['id' => 18, 'name' => 'Finisher'],
            ['id' => 19, 'name' => 'Night Watchman'],
            ['id' => 20, 'name' => 'Powerplay Specialist'],
            ['id' => 21, 'name' => 'Death Over Specialist'],
            ['id' => 22, 'name' => 'Strike Bowler'],
            ['id' => 23, 'name' => 'Pinch Hitter'],
            ['id' => 24, 'name' => 'Part-time Bowler'],
        ];

        foreach ($roles as &$role) {
            $role['sport_type'] = 'cricket';
            $role['created_at'] = $now;
            $role['updated_at'] = $now;
        }

        PlayerRole::insert($roles);
    }
}
