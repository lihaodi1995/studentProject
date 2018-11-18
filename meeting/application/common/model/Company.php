<?php
namespace app\common\model;

use think\Model;

class Company extends Model {
    protected $pk = 'company_id';

    public function companyUnits() {
        return $this->hasMany('CompanyUnit', 'company_id');
    }

    public function companyAdditions() {
        return $this->hasMany('CompanyAddition', 'company_id');
    }

    public function meetings() {
        return $this->hasMany('Meeting', 'company_id');
    }
}
