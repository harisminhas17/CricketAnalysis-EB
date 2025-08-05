<?php

namespace App\Http\Controllers;

use App\Models\Player;
use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

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
                'date_of_birth' => date('Y-m-d', strtotime($request->date_of_birth)),
                'created_at' => now(),
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'message' => 'Error registering player',
                'error' => $e->getMessage()
            ], 200);
        }

        return response()->json([
            'error' => false,
            'message' => 'Player registered successfully' . ' with ' . $request->login_type,
            'records' => $player
        ]);
    }


    public function playerLogin(Request $request)
    {
        $request->validate([
            'email' => 'required',
            'password' => 'required',
            'login_type' => 'required',
            'phone_number' => 'required',
        ]);

        try {

            $player = Player::where('email', $request->email)
                ->first();

            if (!$player) {
                return response()->json([
                    'message' => 'Player not found',
                    'error' => true,
                ], 200);
            }

            // Check login_type separately
            if ($player->login_type !== $request->login_type) {
                return response()->json([
                    'message' => 'Login type mismatch',
                    'error' => true,
                ], 200);
            }

            // Password verify karo
            if (!Hash::check($request->password, $player->password)) {
                return response()->json([
                    'message' => 'Invalid password',
                    'error' => true,
                ], 200);
            }

            // Success response
            return response()->json([
                'error' => false,
                'message' => 'Player Login successful' . ' with ' . $request->login_type,
                'records' => $player
            ], 200);
        } catch (\Exception $e) {
            return response()->json([
                'message' => 'Error logging in player',
                'error' => $e->getMessage()
            ], 200);
        }
    }
}
