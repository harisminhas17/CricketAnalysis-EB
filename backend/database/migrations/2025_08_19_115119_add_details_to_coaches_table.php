<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('coaches', function (Blueprint $table) {
            if (!Schema::hasColumn('coaches', 'name')) {
                $table->string('name', 100)->after('id');
            }
            if (!Schema::hasColumn('coaches', 'email')) {
                $table->string('email')->unique()->after('name');
            }
            if (!Schema::hasColumn('coaches', 'phone')) {
                $table->string('phone', 20)->nullable()->after('email');
            }
            if (!Schema::hasColumn('coaches', 'speciality')) {
                $table->string('speciality', 100)->nullable()->after('phone');
            }
            if (!Schema::hasColumn('coaches', 'experience')) {
                $table->string('experience', 100)->nullable()->after('speciality');
            }
            if (!Schema::hasColumn('coaches', 'password')) {
                $table->string('password')->after('experience');
            }
        });
    }

    public function down(): void
    {
        Schema::table('coaches', function (Blueprint $table) {
            $table->dropColumn(['name', 'email', 'phone', 'speciality', 'experience', 'password']);
        });
    }
};
