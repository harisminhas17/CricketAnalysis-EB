<?php

namespace App\Http\Controllers;

use App\Models\Player;
use Illuminate\Http\Request;
use Illuminate\Routing\Controller;

class AuthController extends Controller
{
    public function playerRegister(Request $request)
    {

        $request->validate([
            'sport_type' => 'required',
            'name' => 'required',
            'email' => 'required',
            'phone_number' => 'required',
            'password' => 'required|min:6',
            'login_type' => 'required',
            'gender' => 'required|in:male,female,other',
            'date_of_birth' => 'required',
        ]);

        try {

            $player = Player::create([
                'sport_type' => $request->sport_type,
                'user_name' => $request->name,
                'email' => $request->email,
                'phone_number' => $request->phone_number,
                'password' => bcrypt($request->password),
                'login_type' => $request->login_type,
                'gender' => $request->gender,
                'date_of_birth' => $request->date_of_birth,
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'message' => 'Error registering player',
                'error' => $e->getMessage()
            ], 200);
        }

        return response()->json([
            'error' => false,
            'message' => 'Player registered successfully' . ' with '. $request->login_type,
            'records' => $player
        ]);
    }
}
