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
            'phone_number' => 'nullable',
            'password' => 'required|min:6',
            'login_type' => 'required',
            'gender' => 'required|in:male,female,other',
            'date_of_birth' => 'required',
        ]);

        // Check if email already exists
        if (Player::where('email', $request->email)
            ->where('login_type', $request->login_type)
            ->where('sport_type', $request->sport_type)
            ->exists()
        ) {
            return response()->json([
                'error' => true,
                'message' => 'Email already exists with ' . $request->login_type . ' for ' . $request->sport_type,
            ], 200);
        }

        // Check if phone number already exists
        if (Player::where('phone_number', $request->phone_number)->exists()) {
            return response()->json([
                'error' => true,
                'message' => 'Phone number ' . $request->phone_number . ' already exists',
            ], 200);
        }


        try {

            $player = Player::create([
                'sport_type' => $request->sport_type,
                'user_name' => $request->name,
                'email' => $request->email,
                'phone_number' => $request->phone_number,
                'password' => Hash::make($request->password),
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
            'message' => 'Player registered successfully' . ' with ' . $request->login_type . ' for ' . $request->sport_type,
            'records' => $player
        ]);
    }

    public function playerLogin(Request $request)
    {
        $request->validate([
            'email' => 'required',
            'password' => 'required',
            'login_type' => 'required',
            'sport_type' => 'required',
            'phone_number' => 'nullable',
        ]);

        try {

            $player = Player::where('email', $request->email)
                ->where('login_type', $request->login_type)
                ->where('sport_type', $request->sport_type)
                ->first();

            if (!$player) {
                return response()->json([
                    'message' => 'Player email not found with ' . $request->login_type . ' for ' . $request->sport_type,
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

            if (!Hash::check($request->password, $player->password)) {
                return response()->json([
                    'message' => 'Invalid password',
                    'error' => true,
                ], 200);
            }

            $token = $player->createToken('PlayerToken', ['*'])->plainTextToken;

            // Success response
            return response()->json([
                'error' => false,
                'message' => 'Player Login successful' . ' with ' . $request->login_type . ' for ' . $request->sport_type,
                'token' => $token,
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
