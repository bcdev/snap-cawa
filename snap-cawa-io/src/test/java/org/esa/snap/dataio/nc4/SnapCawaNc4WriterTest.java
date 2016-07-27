package org.esa.snap.dataio.nc4;

import org.esa.snap.core.dataio.ProductIO;
import org.esa.snap.core.datamodel.Product;

import java.io.File;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class SnapCawaNc4WriterTest {

    public static void main(String[] args) throws Exception {
        final Product testproduct = loadTcwvProduct();
        ProductIO.writeProduct(testproduct, "./BLA_" + testproduct.getName() + ".nc", "NetCDF4-CAWA");
//        ProductIO.writeProduct(testproduct, "./BLA_" + testproduct.getName() + "_nc4beam.nc", "NetCDF4-BEAM");
    }

    private static Product loadTcwvProduct() {
        final String tcwvFilename = "subset_TCWV.nc";
        final String tcwvFilePath = SnapCawaNc4WriterTest.class.getResource(tcwvFilename).getPath();

        Product tcwvProduct = null;
        try {
            Logger.getGlobal().log(Level.INFO, "Reading TCWV file '" + tcwvFilePath + "'...");
            tcwvProduct = ProductIO.readProduct(new File(tcwvFilePath));
        } catch (IOException e) {
            Logger.getGlobal().log(Level.WARNING, "Warning: cannot open or read AOT climatology file.");
        }
        return tcwvProduct;
    }
}
