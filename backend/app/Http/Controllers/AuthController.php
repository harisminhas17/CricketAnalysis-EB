<?php

namespace App\Http\Controllers;

use App\HelperFunctions\HelperFunctions;
use App\Models\Nationality;
use App\Models\Player;
use App\Models\PlayerRole;
use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
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
            'phone' => 'nullable',
            'password' => 'required|min:6',
            'login_type' => 'required',
            'gender' => 'required|in:male,female,other',
            'date_of_birth' => 'required',
            'address' => 'required',
            'nationality_id' => 'required',
            'profile_image' => 'nullable',
            'role_id' => 'nullable|integer',
            'batting_style' => 'nullable',
            'bowling_style' => 'nullable',
            'dominant_hand' => 'nullable',
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
        if (Player::where('phone_number', $request->phone)->exists()) {
            return response()->json([
                'error' => true,
                'message' => 'Phone number ' . $request->phone . ' already exists',
            ], 200);
        }


        try {
            $imagePath = null;
            // Handle profile image upload
            if ($request->hasFile('profile_image')) {
                $imagePath = HelperFunctions::uploadImage($request->file('profile_image'), 'uploads/players/');
            }

            $player = Player::create([
                'sport_type' => $request->sport_type,
                'user_name' => $request->name,
                'email' => $request->email,
                'phone_number' => $request->phone,
                'password' => Hash::make($request->password),
                'login_type' => $request->login_type,
                'gender' => $request->gender,
                'date_of_birth' => date('Y-m-d', strtotime($request->date_of_birth)),
                'address' => $request->address,
                'nationality_id' => $request->nationality_id,
                'profile_image' => $imagePath,
                'player_role_id' => $request->role_id,
                'batting_style' => $request->batting_style,
                'bowling_style' => $request->bowling_style,
                'dominant_hand' => $request->dominant_hand,
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
            'phone' => 'nullable',
        ]);

        try {

            $player = Player::where('email', $request->email)
                ->where('login_type', $request->login_type)
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

    public function getNationalities(Request $request)
    {
        $nationalities = Nationality::select('id', 'name')
            ->orderBy('name')
            ->get();

        if ($nationalities->isEmpty()) {
            return response()->json([
                'error' => true,
                'message' => 'No nationalities found.',
            ], 200);
        }

        return response()->json([
            'error' => false,
            'message' => 'Nationalities fetched successfully.',
            'records' => $nationalities,
        ], 200);
    }

    public function getPlayerRoles(Request $request)
    {
        $roles = PlayerRole::select('id', 'name', 'sport_type')->orderBy('name')->get();

        if ($roles->isEmpty()) {
            return response()->json([
                'error' => true,
                'message' => 'No player roles found.',
            ], 200);
        }
        return response()->json([
            'error' => false,
            'message' => 'Player roles fetched successfully.',
            'records' => $roles,
        ], 200);
    }

    public function updatePlayerProfile(Request $request)
    {
        try {
            $request->validate([
                'user_name'     => 'nullable|string|max:50',
                'address'       => 'nullable|string|max:255',
                'city'          => 'nullable|string|max:50',
                'state'         => 'nullable|string|max:50',
                'zip_code'      => 'nullable|string|max:10',
                'country'       => 'nullable|string|max:50',
                'gender'        => 'nullable|in:male,female,other',
                'date_of_birth' => 'nullable|date',
                'profile_image' => 'nullable|image',
                'dominant_hand' => 'nullable|string|max:10',
                'batting_style' => 'nullable|string|max:50',
                'bowling_style' => 'nullable|string|max:50',
            ]);


            $player = Auth::user();

            if (!$player) {
                return response()->json([
                    'error' => true,
                    'message' => 'Player not authenticated.',
                ], 200);
            }

            if ($request->hasFile('profile_image')) {
                $imagePath = HelperFunctions::uploadImage(
                    $request->file('profile_image'),
                    'profiles'
                );
            }

            $updateData = [];
            if ($request->user_name) $updateData['user_name'] = $request->user_name;
            if ($request->address) $updateData['address'] = $request->address;
            if ($request->city) $updateData['city'] = $request->city;
            if ($request->state) $updateData['state'] = $request->state;
            if ($request->zip_code) $updateData['zip_code'] = $request->zip_code;
            if ($request->country) $updateData['country'] = $request->country;
            if ($request->gender) $updateData['gender'] = $request->gender;
            if ($request->date_of_birth) $updateData['date_of_birth'] = date('Y-m-d', strtotime($request->date_of_birth));
            if ($request->dominant_hand) $updateData['dominant_hand'] = $request->dominant_hand;
            if ($request->batting_style) $updateData['batting_style'] = $request->batting_style;
            if ($request->bowling_style) $updateData['bowling_style'] = $request->bowling_style;
            if (isset($imagePath)) $updateData['profile_image'] = $imagePath;

            try {
                Player::where('id', $player->id)->update($updateData);
                $player = Player::find($player->id);
            } catch (\Exception $e) {
                return response()->json([
                    'error' => true,
                    'message' => 'Failed to update profile.',
                    'exception' => $e->getMessage(),
                ], 200);
            }

            return response()->json([
                'error' => false,
                'message' => 'Player profile updated successfully.',
                'records' => $player,
            ], 200);
        } catch (\Exception $e) {
            return response()->json([
                'error' => true,
                'message' => 'Failed to update profile.',
                'exception' => $e->getMessage(),
            ], 200);
        }
    }


    public function checkCredentials(Request $request)
    {
        $request->validate([
            'email' => 'required',
            'password' => 'required',
        ]);
    }
}
