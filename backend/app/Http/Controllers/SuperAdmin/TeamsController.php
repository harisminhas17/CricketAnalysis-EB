<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use App\Models\SuperAdmin;
use App\Models\Team;
use App\HelperFunctions\HelperFunctions;
//------------------ Teams -----------------
//------------------Add team---------------------
class SuperAdminController extends Controller
{
    public function addTeam(Request $request)
    {
        $validated = $request->validate([
            'name'        => 'required|string|max:255',
            'sport_type'  => 'required|string|max:255',
            'club_id'     => 'nullable|integer',
            'coach_id'    => 'nullable|integer',
            'level'       => 'nullable|string|max:255',
        ]);

        $team = Team::create($validated);

        return response()->json([
            'error'   => false,
            'message' => 'Team created successfully',
            'records'    => $team
        ], 201);
    }
//------------------Edit team---------------------
public function editTeam(Request $request)
{
    $validated = $request->validate([
        'team_id'     => 'required|integer|exists:teams,id',
        'name'        => 'sometimes|string|max:255',
        'sport_type'  => 'sometimes|string|max:255',
        'club_id'     => 'nullable|integer',
        'coach_id'    => 'nullable|integer',
        'level'       => 'sometimes|string|max:255',
    ]);

    $team = Team::findOrFail($validated['team_id']);

    // Remove team_id from update array so it doesn't try to overwrite PK
    unset($validated['team_id']);

    $team->update($validated);

    return response()->json([
        'error'   => false,
        'message' => 'Team updated successfully',
        'records'    => $team
    ], 200);
    
}
//------------------Delete team---------------------
public function deleteTeam(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'team_id' => 'required|integer',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'error'   => true,
                'message' => 'Validation failed',
                'records' => $validator->errors()
            ], 422);
        }

        $team = Team::findOrFail($request->team_id);
        $team->delete();

        return response()->json([
            'error'   => false,
            'message' => 'Team deleted successfully: ' . $request->team_id,
        ]);
}
}